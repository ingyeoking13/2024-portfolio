from kubernetes import client, config
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Dict, List, Optional

class K8SConfigure:
    _client = None

    def __init__(self) -> None:
        self.load_config()

    def load_config(self):
        if self._client is None:
            config.load_kube_config()
            self._client = client.CoreV1Api()
        
        return self._client
    
    @property
    def client(self):
        return self._client
        
