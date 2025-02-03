import os
import time

import requests
from loguru import logger
from dotenv import load_dotenv
import cv2

load_dotenv()


def upload_image(http_url, fingerprint, token, image_data):
    logger.debug("Upload image Start")
    response = requests.put(
        http_url,
        headers={
            "accept": "*/*",
            "content-type": "image/jpg",
            "fingerprint": fingerprint,
            "token": token,
        },
        data=image_data,
        stream=True,
        # verify=False,
    )
    return response


def get_image(rtsp_url: str):
    logger.debug("Get image start")
    cap = cv2.VideoCapture(rtsp_url)

    cap.grab()

    success, image = cap.retrieve()
    if success:
        return cv2.imencode('.jpg', image)
    return success, None


def main():
    logger.info("prusa-connect-rtsp starting...")
    interval = int(os.getenv("PRUSA_CONNECT_UPLOAD_INTERVAL", "30").strip().strip("\"'"))  # Seconds

    rtsp_url = os.getenv("PRUSA_CONNECT_RTSP_URL").strip().strip("\"'")
    if not rtsp_url:
        raise ValueError("ENVVAR PRUSA_CONNECT_RTSP_URL is required")

    snapshot_api_url = os.getenv("PRUSA_CONNECT_URL", "https://connect.prusa3d.com/c/snapshot").strip().strip("\"'")
    if not snapshot_api_url:
        raise ValueError("ENVVAR PRUSA_CONNECT_URL is required")
    fingerprint = os.getenv("PRUSA_CONNECT_FINGERPRINT").strip().strip("\"'")
    if not fingerprint:
        raise ValueError("ENVVAR PRUSA_CONNECT_FINGERPRINT is required. Set it to a random UUID.")
    api_token = os.getenv("PRUSA_CONNECT_TOKEN").strip().strip("\"'")
    if not api_token:
        raise ValueError("ENVVAR PRUSA_CONNECT_TOKEN is required")

    while True:
        try:
            success, image = get_image(rtsp_url)
            if success:
                upload_response = upload_image(snapshot_api_url, fingerprint, api_token, image.data)

                if not (200 < upload_response.status_code < 299):
                    logger.error("Failed to upload image to prusa connect")
                    logger.debug(str(upload_response.content))
                else:
                    logger.debug("Image uploaded")
            else:
                logger.error("Failed to retrieve image from RTSP")

        except Exception as e:
            logger.error(f"Exception caught: {e}")
        time.sleep(interval)


if __name__ == "__main__":
    main()
