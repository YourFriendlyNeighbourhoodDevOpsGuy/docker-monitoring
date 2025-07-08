provider "aws" {
  region = var.aws_region
}

# Verify sender email identity
resource "aws_ses_email_identity" "sender" {
  email = var.sender_email
}

# Verify recipient email identity
resource "aws_ses_email_identity" "recipient" {
  email = var.recipient_email
}

output "sender_verification_status" {
  value = aws_ses_email_identity.sender.verification_status
}

output "recipient_verification_status" {
  value = aws_ses_email_identity.recipient.verification_status
}
