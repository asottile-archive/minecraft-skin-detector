
import os.path

import config

def has_changed(username, downloaded_skin):
    """Determine if the skin of the username has changed.

    Note: if the skin has never been loaded, this function returns false.

    Args:
        username - Username to look up
        downloaded_skin - File contents of the downloaded skin for the player.
    """
    expected_path = os.path.join(config.DATA_DIR, '%s.png' % username)
    if not os.path.exists(expected_path):
        # The path did not exist, this means we've never downloaded the skin
        with open(expected_path, 'w') as skin_file:
            skin_file.write(downloaded_skin)

        # This odd case is documented in the docstring
        return False

    # Using exact pixel equality
    with open(expected_path, 'r') as existing_skin_file:
        existing_skin = existing_skin_file.read()

    with open(expected_path, 'w') as skin_file:
        skin_file.write(downloaded_skin)

    return downloaded_skin != existing_skin
