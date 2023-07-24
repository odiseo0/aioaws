from dataclasses import dataclass
from typing import TYPE_CHECKING

from httpx import AsyncClient, Response

from .core import AWSV4AuthFlow


if TYPE_CHECKING:
    from ._utils import ConfigProtocol


@dataclass
class SecretsManagerConfig:
    aws_access_key: str
    aws_secret_key: str
    aws_region: str


class SecretsManagerClient:
    __slots__ = 'client', 'auth', 'service_url', 'config'

    def __init__(self, client: AsyncClient, config: 'ConfigProtocol') -> None:
        self.client = client
        self.auth = AWSV4AuthFlow(
            aws_access_key=config.aws_access_key, 
            aws_secret_key=config.aws_secret_key, 
            region=config.aws_region,
            service='secretsmanager'
        )
        self.service_url = f'https://secretsmanager.{config.aws_region}.amazonaws.com'

    async def get_secret_value(self, secret_id: str) -> Response:
        response = await self.client.post(
            self.service_url,
            content=f'{{"SecretId": "{secret_id}"}}',
            auth=self.auth,
            headers={
                'x-amz-target': 'secretsmanager.GetSecretValue', 
                'content-type': 'application/x-amz-json-1.1'
            }
        )

        return response
