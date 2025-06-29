from pydantic import BaseModel


class AudioDeviceDto(BaseModel):
    audio_device: str