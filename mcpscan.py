import argparse
import asyncio
import sys
from fastmcp import Client

parser = argparse.ArgumentParser()
parser.add_argument("--host", help="Target host as ip:port, e.g. 172.17.0.2:8000")
parser.add_argument("--list", action="store_true",
                    help="List all resources, resource templates and tools (default)")
parser.add_argument("--resource", help='Read a resource, e.g. --resource "resource://items"')
parser.add_argument("--tool", nargs="+", metavar="ARG",
                    help='Call a tool: --tool TOOL_NAME key=value [key=value ...] '
                         '(e.g. --tool execute_server_command command=date)')
parser.add_argument("--encode", action="store_true",
                    help="URL-encode spaces (replace ' ' with %%20) in --resource and tool params")
args = parser.parse_args()

if not args.host:
    parser.print_help()
    sys.exit(1)

client = Client(f"http://{args.host}/mcp/")

def enc(value):
    return value.replace(" ", "%20") if args.encode else value

def indent(text):
    return "\n".join("      " + line for line in text.strip().splitlines())

def parse_tool_args(tokens):
    name = tokens[0]
    params = {}
    for tok in tokens[1:]:
        if "=" not in tok:
            print(f"[-] Invalid parameter '{tok}', expected key=value")
            sys.exit(1)
        key, value = tok.split("=", 1)
        params[key] = enc(value)
    return name, params

async def list_all():
    resources = await client.list_resources()
    resource_templates = await client.list_resource_templates()
    tools = await client.list_tools()

    print("=" * 50)
    print("[*] RESOURCES")
    print("=" * 50)
    for resource in resources:
        print(f"\n[+] {resource.name}")
        print(f"    [uri]  {resource.uri}")
        if resource.mimeType:
            print(f"    [mime] {resource.mimeType}")
        print(indent(resource.description))

    print("\n" + "=" * 50)
    print("[*] RESOURCE TEMPLATES")
    print("=" * 50)
    for rt in resource_templates:
        print(f"\n[+] {rt.name}")
        print(f"    [uri]  {rt.uriTemplate}")
        if rt.mimeType:
            print(f"    [mime] {rt.mimeType}")
        print(indent(rt.description))

    print("\n" + "=" * 50)
    print("[*] TOOLS")
    print("=" * 50)
    for tool in tools:
        params = list(tool.inputSchema.get('properties', {}).keys())
        print(f"\n[+] {tool.name}({', '.join(params)})")
        schema = tool.inputSchema.get('properties', {})
        for name, spec in schema.items():
            ptype = spec.get('type', '?')
            required = name in tool.inputSchema.get('required', [])
            req = "required" if required else "optional"
            print(f"    [arg]  {name}: {ptype} ({req})")
        print(indent(tool.description))

async def read_resource(uri):
    uri = enc(uri)
    print(f"[*] Reading {uri}")
    try:
        result = await client.read_resource(uri)
        print(result[0].text)
    except Exception as e:
        print(f"[-] {e}")

async def call_tool(name, params):
    print(f"[*] Calling {name}({', '.join(f'{k}={v}' for k, v in params.items())})")
    try:
        result = await client.call_tool(name, params)
        print(result.content[0].text)
    except Exception as e:
        print(f"[-] {e}")

async def main():
    async with client:
        if args.tool:
            name, params = parse_tool_args(args.tool)
            await call_tool(name, params)
        elif args.resource:
            await read_resource(args.resource)
        else:
            await list_all()

asyncio.run(main())
