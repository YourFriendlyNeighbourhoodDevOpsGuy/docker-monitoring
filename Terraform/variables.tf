variable "aws_region" {
  description = "AWS region to use for SES"
  default     = "ap-south-1"
}

variable "sender_email" {
  description = "Email address to use as sender"
  type        = string
}

variable "recipient_email" {
  description = "Email address to use as recipient"
  type        = string
}
