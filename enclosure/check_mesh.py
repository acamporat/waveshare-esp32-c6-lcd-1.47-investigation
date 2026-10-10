"""Check exported solids; no claim of physical fit or structural validation."""
from pathlib import Path
import json, sys
root = Path(__file__).resolve().parent
import trimesh
def components(mesh):
    parent = list(range(len(mesh.faces)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in mesh.face_adjacency:
        parent[find(int(a))] = find(int(b))
    return len({find(i) for i in range(len(parent))})
results = {}
for path in sorted((root / 'stl').glob('*.stl')):
    mesh = trimesh.load_mesh(path)
    result = {
        'watertight': bool(mesh.is_watertight),
        'winding_consistent': bool(mesh.is_winding_consistent),
        'connected_solids': components(mesh),
        'bounds_mm': mesh.bounds.tolist(),
        'extents_mm': mesh.extents.tolist(),
        'volume_mm3': float(mesh.volume),
        'triangles': len(mesh.faces),
    }
    results[path.name] = result
    assert result['watertight'] and result['winding_consistent'], (path, result)
    assert result['connected_solids'] == 1 and mesh.volume > 0, (path, result)
(root / 'mesh-check.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
