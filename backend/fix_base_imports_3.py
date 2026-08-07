import os

filepath = 'backend/app/db/base.py'
if os.path.exists(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    content = content.replace(
        'from app.models.digital_twin import SimulationScenario, SimulationResult, CVOptimizationRecommendation',
        'from app.models.digital_twin import SimulationScenario, SimulationResult, OptimizationRecommendation'
    )
    
    with open(filepath, 'w') as f:
        f.write(content)
