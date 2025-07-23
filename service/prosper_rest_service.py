# service/prosper_rest_service.py

import requests
import logging
from dacite import from_dict, Config
from dataclasses import dataclass


@dataclass
class OAuthToken:
    access_token: str
    token_type: str
    refresh_token: str
    expires_in: int


class OauthTokenHolder:
    def __init__(self):
        self.token = None

    def set_oauth_token(self, token):
        self.token = token

    def get_oauth_token(self):
        return self.token

    def is_token_valid(self):
        return self.token is not None and "expires_in" in self.token and self.token["expires_in"] > 0


class ProsperRestService:
    def __init__(self, prosper_config, o_auth_token_holder):
        self.prosper_config = prosper_config
        self.o_auth_token_holder = o_auth_token_holder
        self.logger = logging.getLogger(__name__)

    def get_base_url(self):
        # Implement this method to return the base URL
        return self.prosper_config.base_url

    def get_http_headers(self):
        if (
                self.o_auth_token_holder.get_oauth_token() is None or
                not self.o_auth_token_holder.get_oauth_token().get("access_token")
        ):
            self.init_token()
        token = self.o_auth_token_holder.get_oauth_token().get("access_token")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"bearer {token}"
        }
        return headers

    def init_token(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        url = f"{self.get_base_url()}/v1/security/oauth/token"
        data = {
            "grant_type": "password",
            "client_id": self.prosper_config.client_id,
            "client_secret": self.prosper_config.client_secret,
            "username": self.prosper_config.username,
            "password": self.prosper_config.password
        }

        self.logger.info("Initializing OAuth Token...")
        response = requests.post(url, headers=headers, data=data)
        if not response.ok or not response.json().get("access_token"):
            raise Exception(
                f"Exception initializing Prosper OAuth Token {response.status_code}"
            )

        self.o_auth_token_holder.set_oauth_token(response.json())
        self.logger.info(
            "OAuth Token retrieved with expiry in %s seconds.",
            self.o_auth_token_holder.get_oauth_token().get("expires_in")
        )

    def get_entity(self, url, data_class):
        headers = self.get_http_headers()
        response = requests.get(url, headers=headers)
        if response.status_code in (401, 403):
            self.logger.info("Expired access token detected, re-initializing token...")
            self.init_token()
            headers = self.get_http_headers()
            response = requests.get(url, headers=headers)
        if not response.ok:
            raise Exception(f"Error retrieving {data_class.__name__}: {response.status_code}")
        return from_dict(data_class=data_class, data=response.json(), config=Config(strict=False))
