import logging

logging.basicConfig(level=logging.DEBUG,
                    format="[%()s |%(asctime)s | %(levelname)s | %(massage)s]",
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler("app.log", "a")
                    ])

logger = logging.getLogger(__name__)