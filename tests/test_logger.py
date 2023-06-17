from net_operations.lib.logger import own_logger, logfile


def test_own_logger():
    values = [(own_logger.info, 'TEST INFO MESSAGE', True),
              (own_logger.error, 'TEST ERROR MESSAGE', True),
              (own_logger.debug, 'TEST DEBUG MESSAGE', False)]

    for logger, message, state in values:
        logger(message)
        with open(logfile) as src:
            if state:
                assert message in src.read()
            else:
                assert message not in src.read()
