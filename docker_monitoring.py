import docker
import logging
import time
import signal
import sys
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# ================== Configuration ==================

CPU_USAGE_THRESHOLD = 80.0  # in percentage
CHECK_INTERVAL = 5  # in seconds

# AWS SES configuration
SES_REGION = 'us-east-1'  # change as per your SES region
SENDER_EMAIL = 'sender@example.com'  # must be verified in SES
RECIPIENT_EMAIL = 'recipient@example.com'  # must be verified in SES
EMAIL_SUBJECT = 'Docker Container High CPU Usage Alert'

# ================== Logging Setup ==================

logging.basicConfig(
    filename='docker_cpu_monitor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================== Signal Handling ==================

def signal_handler(sig, frame):
    print("Stopping container monitor...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# ================== Helper Functions ==================

def get_cpu_percentage(stats):
    try:
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                    stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                       stats['precpu_stats']['system_cpu_usage']
        cpu_count = len(stats['cpu_stats']['cpu_usage'].get('percpu_usage', []))

        if system_delta > 0.0 and cpu_delta > 0.0:
            return (cpu_delta / system_delta) * cpu_count * 100.0
    except KeyError as e:
        logging.error(f"Error parsing CPU stats: {e}")
    return 0.0

def send_email_alert(container_name, cpu_percent):
    body_text = (
        f"ALERT: Docker container '{container_name}' is using {cpu_percent:.2f}% CPU.\n"
        f"This exceeds the defined threshold of {CPU_USAGE_THRESHOLD}%."
    )

    client = boto3.client('ses', region_name=SES_REGION)

    try:
        response = client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [RECIPIENT_EMAIL]},
            Message={
                'Subject': {'Data': EMAIL_SUBJECT},
                'Body': {'Text': {'Data': body_text}}
            }
        )
        logging.info(f"Email sent: Message ID {response['MessageId']}")
    except (BotoCoreError, ClientError) as e:
        logging.error(f"Error sending email alert: {e}")

# ================== Main Monitoring Function ==================

def monitor_containers():
    try:
        client = docker.from_env()

        while True:
            containers = client.containers.list()
            for container in containers:
                try:
                    stats = container.stats(stream=False)
                    cpu_percent = get_cpu_percentage(stats)

                    if cpu_percent > CPU_USAGE_THRESHOLD:
                        alert_msg = (
                            f"ALERT: Container {container.name} CPU usage is {cpu_percent:.2f}% "
                            f"(threshold: {CPU_USAGE_THRESHOLD}%)"
                        )
                        print(alert_msg)
                        logging.warning(alert_msg)
                        send_email_alert(container.name, cpu_percent)
                    else:
                        logging.info(f"Container {container.name} CPU usage: {cpu_percent:.2f}%")
                except Exception as e:
                    logging.error(f"Error monitoring container {container.name}: {e}")
            time.sleep(CHECK_INTERVAL)
    except docker.errors.DockerException as de:
        logging.error(f"Could not connect to Docker: {de}")
    except Exception as ex:
        logging.error(f"Unhandled exception: {ex}")

# ================== Entry Point ==================

if __name__ == "__main__":
    print("Starting Docker container CPU monitor...")
    monitor_containers()
