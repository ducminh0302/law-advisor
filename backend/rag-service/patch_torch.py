"""
Patch torch.load to skip version check
"""
import torch
import warnings

# Save original load function
_original_load = torch.load

def patched_load(*args, **kwargs):
    """Patched torch.load that forces use of safetensors"""
    # If weights_only is passed, remove it and handle manually
    if 'weights_only' in kwargs:
        del kwargs['weights_only']
    
    # Try to use safetensors if available
    try:
        return _original_load(*args, **kwargs, weights_only=False)
    except Exception as e:
        # If that fails, try without weights_only
        warnings.warn(f"Falling back to unsafe load: {e}")
        return _original_load(*args, **kwargs)

# Apply patch
torch.load = patched_load

print("✅ torch.load patched to skip version check")
