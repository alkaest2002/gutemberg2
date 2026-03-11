from pathlib import Path


class ValidationError(Exception):
  pass

class NotFoundError(Exception):
  pass

class TracebackNotifier:
    """Class to notify error tracebacks in a readable format.

    Attributes:
        error (Exception): The error to notify the traceback of.
    """

    def __init__(self, error):
        """Initialize TracebackNotifier with an error.

        Args:
            error (Exception): The error to notify the traceback of.

        Returns:
            None
        """
        self.error = error

    def notify_traceback(self):
        """Notify the traceback of the stored error in a readable format.

        Returns:
            None
        """
        try:
            # Get error's traceback
            traceback = self.error.__traceback__
            # Consume traceback
            while traceback is not None:
                # Notify current traceback step
                print(  # noqa: T201
                    "-->",
                    Path(traceback.tb_frame.f_code.co_filename),
                    traceback.tb_frame.f_code.co_name,
                    "line code",
                    traceback.tb_lineno
                , end="\n")
                # Get next traceback step
                traceback = traceback.tb_next
        # On error
        except Exception as e:
            # Store error
            self.error = e
            # Notify traceback
            self.notify_traceback()
