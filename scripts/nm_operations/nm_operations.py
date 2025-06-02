import logging
from netmiko import ConnectHandler
from netmiko.exceptions import ConnectionException, NetmikoTimeoutException, NetmikoAuthenticationException, SSHException


def connect_to_device(device_info):
    """
    Connect to a network device using Netmiko.

    Args:
        device_info (dict): A dictionary containing device connection details.

    Returns:
        netmiko.ConnectHandler: An active connection handler.
    """
    try:
        connection = ConnectHandler(**device_info)
        logging.info(f"Successfully connected to {device_info['host']}")
        return connection
    except NetmikoAuthenticationException as auth_err:
        logging.error(f"Authentication failed for {device_info['host']}: {auth_err}")
        return None
    except NetmikoTimeoutException as timeout_err:
        logging.error(f"Connection timed out for {device_info['host']}: {timeout_err}")
        return None
    except ConnectionException as conn_err:
        logging.error(f"Connection error for {device_info['host']}: {conn_err}")
        return None
    except SSHException as ssh_err:
        logging.error(f"SSH error while connecting to {device_info['host']}: {ssh_err}")
        return None
    except Exception as e:
        logging.error(f"Failed to connect to {device_info['host']}: {e}")
        return None


def disconnect_from_device(connection):
    """
    Disconnect from a network device.

    Args:
        connection (netmiko.ConnectHandler): An active connection handler.
    """
    if connection:
        connection.disconnect()
        logging.info("Disconnected successfully.")
    else:
        logging.info("No active connection to disconnect.")


def execute_command(connection, command):
    """
    Execute a command on the connected network device.

    Args:
        connection (netmiko.ConnectHandler): An active connection handler.
        command (str): The command to execute.

    Returns:
        str: The output of the command execution.
    """
    if not connection:
        logging.info("No active connection to execute command.")
        return None

    try:
        output = connection.send_command(command)
        logging.info(f"Command executed successfully: {command}")
        return output
    except Exception as e:
        logging.error(f"Failed to execute command '{command}': {e}")
        return None


def execute_commands(connection, commands):
    """
    Execute multiple commands on the connected network device.

    Args:
        connection (netmiko.ConnectHandler): An active connection handler.
        commands (list): A list of commands to execute.

    Returns:
        dict: A dictionary with command as key and output as value.
    """
    if not connection:
        logging.info("No active connection to execute commands.")
        return None

    results = {}
    for command in commands:
        try:
            output = connection.send_command(command)
            results[command] = output
            logging.info(f"Command executed successfully: {command}")
        except Exception as e:
            logging.error(f"Failed to execute command '{command}': {e}")
            results[command] = None
    return results


def configure_device(connection, configuration_commands):
    """
    Configure a network device with a list of commands.

    Args:
        connection (netmiko.ConnectHandler): An active connection handler.
        configuration_commands (list): A list of configuration commands.

    Returns:
        str: The output of the configuration commands execution.
    """
    if not connection:
        logging.info("No active connection to configure device.")
        return None

    try:
        output = connection.send_config_set(configuration_commands)
        logging.info("Configuration commands executed successfully.")
        return output
    except Exception as e:
        logging.error(f"Failed to configure device: {e}")
        return None