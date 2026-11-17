# DeepShovel WWW 2027 on macOS

The official site is [deepshovel.iiot-shxt.xyz](https://deepshovel.iiot-shxt.xyz/).
For a local instance, follow the [self-hosting guide](../docs/SELF_HOSTING.md).
The macOS deployment tooling uses loopback ports 8200 for Web and 8211 for the
Compiler.

Prepare the local Worker and Compiler environments:

```sh
python3 scripts/setup-local-config.py
npm run install:ci
```

Set the model provider keys in `compiler/.env.local`. To publish your own
macOS instance, set `subdomain` and `public_url` in `local-public.json` to
a hostname you control. Run `make public-install` to install the runtime,
tunnel, and menu-bar controller, or `make public-update` to update it.

```sh
make public-status
make public-open
make public-restart
make public-logs
```

The runtime, data, credentials, and logs are under
`~/Library/Application Support/DeepShovel WWW 2027/`. The LaunchAgents use
the namespace `xyz.iiot-shxt.deepshovel-www2027`.
