# 0x00. Personal Data

## Overview

This project focuses on managing personal data with a strong emphasis on security and privacy. It covers the handling of Personally Identifiable Information (PII), implementing logging mechanisms, and securing user passwords. 

## Resources

Before diving into the implementation, make sure to read or watch the following resources to understand the key concepts:

- [What Is PII, non-PII, and Personal Data?](#https://piwik.pro/blog/what-is-pii-personal-data/)
- [Logging Documentation](https://docs.python.org/3/library/logging.html) 
- [bcrypt Package](https://github.com/pyca/bcrypt/)
- [Logging to Files, Setting Levels, and Formatting](https://www.youtube.com/watch?v=-ARI4Cz-awo) 

## Learning Objectives

By the end of this project, you should be able to:

1. **Examples of Personally Identifiable Information (PII):**
   - Identify and explain examples of PII and its importance in data privacy.

2. **Implement a Log Filter to Obfuscate PII Fields:**
   - Develop a logging filter that masks or obfuscates PII fields to prevent sensitive information from being exposed in logs.

3. **Encrypt a Password and Check Input Password Validity:**
   - Use `bcrypt` to securely hash and verify passwords, ensuring that passwords are stored and validated securely.

4. **Authenticate to a Database Using Environment Variables:**
   - Configure your application to authenticate to a database using environment variables for secure credential management.
