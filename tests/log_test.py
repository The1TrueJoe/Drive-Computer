import logging

def test():
    logger = logging.getLogger("tester")

    # Print to file
    file_handler = logging.FileHandler("logs/test.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(threadName)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

    logger.debug("Test2")