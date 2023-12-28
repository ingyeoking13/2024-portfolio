from pydantic import BaseModel, Field
from typing import Optional

class KubeContainer(BaseModel):
    pass

class KubePodStatus(BaseModel):
    host_ip: Optional[str] = Field(alias='_host_ip')
    phase: Optional[str] = Field(alias='_phase')
    pod_ip: Optional[str] = Field(alias='_pod_ip')

class KubePodMetadata(BaseModel):
    namespace: Optional[str] = Field(alias='_namespace')
    labels: Optional[dict] = Field(alias='_labels')
    name: Optional[str] = Field(alias='_name')

class KubePod(BaseModel):
    status: KubePodStatus
    metadata: KubePodMetadata