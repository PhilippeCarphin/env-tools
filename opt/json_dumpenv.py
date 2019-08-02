import json
import os

print(json.dumps(dict(os.environ), indent=4, sort_keys=True))
