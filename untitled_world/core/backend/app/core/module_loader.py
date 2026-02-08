"""
Module loader for dynamic module registration and loading.
"""
import json
import importlib
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from fastapi import APIRouter


@dataclass
class ModuleMetadata:
    """Module metadata from module.json."""
    name: str
    version: str
    display_name: str
    description: str
    author: str
    type: str
    dependencies: Dict[str, Any]
    backend: Dict[str, Any]
    frontend: Dict[str, Any]
    permissions: List[str]
    config: Dict[str, Any]


class ModuleLoader:
    """Loads and manages platform modules."""

    def __init__(self, modules_dir: str = "modules", customers_dir: str = "customers"):
        self.modules_dir = Path(modules_dir)
        self.customers_dir = Path(customers_dir)
        self.loaded_modules: Dict[str, ModuleMetadata] = {}
        self.module_routers: Dict[str, APIRouter] = {}

    def discover_modules(self) -> List[str]:
        """Discover available modules in modules directory."""
        if not self.modules_dir.exists():
            return []

        modules = []
        for module_path in self.modules_dir.iterdir():
            if module_path.is_dir():
                module_json = module_path / "module.json"
                if module_json.exists():
                    modules.append(module_path.name)

        return modules

    def load_module_metadata(self, module_name: str) -> Optional[ModuleMetadata]:
        """Load module metadata from module.json."""
        module_json_path = self.modules_dir / module_name / "module.json"

        if not module_json_path.exists():
            return None

        try:
            with open(module_json_path, 'r') as f:
                data = json.load(f)

            return ModuleMetadata(
                name=data.get('name', module_name),
                version=data.get('version', '0.0.0'),
                display_name=data.get('displayName', module_name),
                description=data.get('description', ''),
                author=data.get('author', ''),
                type=data.get('type', 'standard'),
                dependencies=data.get('dependencies', {}),
                backend=data.get('backend', {}),
                frontend=data.get('frontend', {}),
                permissions=data.get('permissions', []),
                config=data.get('config', {}),
            )
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading module {module_name}: {e}")
            return None

    def load_module(self, module_name: str) -> bool:
        """Load a module and its components."""
        metadata = self.load_module_metadata(module_name)
        if not metadata:
            return False

        # Load backend components if enabled
        if metadata.backend.get('enabled', False):
            self._load_backend_components(module_name, metadata)

        self.loaded_modules[module_name] = metadata
        return True

    def _load_backend_components(self, module_name: str, metadata: ModuleMetadata):
        """Load backend API routes and models for a module."""
        module_path = self.modules_dir / module_name / "backend"

        if not module_path.exists():
            return

        try:
            # Import API routes using file path (works with hyphenated module names)
            routes = metadata.backend.get('routes', [])
            for route_file in routes:
                # Use spec_from_file_location to handle module names with hyphens
                api_file_path = module_path / "api.py"
                if api_file_path.exists():
                    spec = importlib.util.spec_from_file_location(
                        f"{module_name}_api",
                        api_file_path
                    )
                    api_module = importlib.util.module_from_spec(spec)
                    sys.modules[f"{module_name}_api"] = api_module
                    spec.loader.exec_module(api_module)

                    if hasattr(api_module, 'router'):
                        api_prefix = metadata.backend.get('apiPrefix', f'/api/v1/{module_name}')
                        self.module_routers[module_name] = {
                            'router': api_module.router,
                            'prefix': api_prefix,
                            'tags': [metadata.display_name]
                        }

            # Import models (they will auto-register with SQLAlchemy)
            models = metadata.backend.get('models', [])
            for model_file in models:
                models_file_path = module_path / "models.py"
                if models_file_path.exists():
                    spec = importlib.util.spec_from_file_location(
                        f"{module_name}_models",
                        models_file_path
                    )
                    models_mod = importlib.util.module_from_spec(spec)
                    sys.modules[f"{module_name}_models"] = models_mod
                    spec.loader.exec_module(models_mod)

        except Exception as e:
            print(f"Error importing module {module_name}: {e}")
            import traceback
            traceback.print_exc()

    def load_customer_config(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Load customer configuration."""
        config_path = self.customers_dir / customer_id / "config.json"

        if not config_path.exists():
            return None

        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading customer config {customer_id}: {e}")
            return None

    def get_enabled_modules_for_customer(self, customer_id: str) -> List[str]:
        """Get list of enabled modules for a customer."""
        config = self.load_customer_config(customer_id)
        if not config:
            return []

        return config.get('modules', {}).get('enabled', [])

    def get_module_config_for_customer(
        self,
        customer_id: str,
        module_name: str
    ) -> Dict[str, Any]:
        """Get module configuration for a specific customer."""
        config = self.load_customer_config(customer_id)
        if not config:
            return {}

        module_configs = config.get('modules', {}).get('config', {})
        return module_configs.get(module_name, {})

    def register_modules_with_app(self, app):
        """Register all loaded module routers with FastAPI app."""
        for module_name, router_data in self.module_routers.items():
            app.include_router(
                router_data['router'],
                prefix=router_data['prefix'],
                tags=router_data['tags']
            )

    def get_module_metadata(self, module_name: str) -> Optional[ModuleMetadata]:
        """Get metadata for a loaded module."""
        return self.loaded_modules.get(module_name)

    def get_all_loaded_modules(self) -> Dict[str, ModuleMetadata]:
        """Get all loaded modules and their metadata."""
        return self.loaded_modules.copy()


# Global module loader instance
# Use absolute paths to find modules directory at project root
_project_root = Path(__file__).parent.parent.parent.parent.parent
module_loader = ModuleLoader(
    modules_dir=str(_project_root / "modules"),
    customers_dir=str(_project_root / "customers")
)
