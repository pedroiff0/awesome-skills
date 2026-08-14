# my-plugin

## What it adds
- command `do-thing`: <what it does>
- hook `post-edit`: runs lint after edits

## Usage
Agent calls `do-thing <args>`. Output is JSON on stdout.

## Security
- No secrets in args; read from env.
- Fail closed (non-zero exit) on error.
