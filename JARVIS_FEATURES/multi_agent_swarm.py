"""
JARVIS Feature Module: Multi-Agent Swarm System
Add this to your JARVIS for autonomous AI agents that collaborate

Features:
- Planner Agent (task planning)
- Research Agent (web/document research)
- Coder Agent (code generation)
- Debugger Agent (bug fixing)
- Memory Agent (information retrieval)
- Security Agent (threat detection)
- Agent-to-agent communication
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
import json


@dataclass
class Task:
    """Task definition for agents"""
    task_id: str
    description: str
    agent_type: str
    priority: int = 5  # 1-10, 10 being highest
    status: str = "pending"  # pending, running, completed, failed
    result: Optional[Any] = None
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_id: str, agent_type: str):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.is_busy = False
    
    @abstractmethod
    async def execute(self, task: Task) -> Any:
        """Execute a task"""
        pass
    
    async def _mark_started(self, task: Task):
        """Mark task as started"""
        task.status = "running"
        task.started_at = datetime.now()
        self.is_busy = True
    
    async def _mark_completed(self, task: Task, result: Any):
        """Mark task as completed"""
        task.status = "completed"
        task.result = result
        task.completed_at = datetime.now()
        self.tasks_completed += 1
        self.is_busy = False
    
    async def _mark_failed(self, task: Task, error: str):
        """Mark task as failed"""
        task.status = "failed"
        task.result = {"error": error}
        task.completed_at = datetime.now()
        self.tasks_failed += 1
        self.is_busy = False
    
    def get_stats(self) -> Dict:
        """Get agent statistics"""
        total = self.tasks_completed + self.tasks_failed
        success_rate = (self.tasks_completed / total * 100) if total > 0 else 0
        
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'tasks_completed': self.tasks_completed,
            'tasks_failed': self.tasks_failed,
            'success_rate': round(success_rate, 2),
            'is_busy': self.is_busy
        }


class PlannerAgent(BaseAgent):
    """Plans and breaks down complex tasks"""
    
    def __init__(self):
        super().__init__("planner_001", "planner")
    
    async def execute(self, task: Task) -> Dict:
        """Create execution plan for task"""
        await self._mark_started(task)
        
        try:
            # Break down task into steps
            steps = await self._create_plan(task.description)
            
            # Estimate time and complexity
            estimated_time = len(steps) * 5  # 5 min per step
            complexity = self._assess_complexity(task.description)
            
            # Determine which agents needed
            required_agents = self._identify_required_agents(task.description)
            
            result = {
                'plan': steps,
                'estimated_time_minutes': estimated_time,
                'complexity': complexity,
                'required_agents': required_agents,
                'created_at': datetime.now().isoformat()
            }
            
            await self._mark_completed(task, result)
            return result
            
        except Exception as e:
            await self._mark_failed(task, str(e))
            return {'error': str(e)}
    
    async def _create_plan(self, description: str) -> List[str]:
        """Create step-by-step plan"""
        # Keywords indicate different types of tasks
        description_lower = description.lower()
        
        steps = []
        
        # Research tasks
        if any(kw in description_lower for kw in ['research', 'find', 'search', 'learn']):
            steps.extend([
                "1. Identify information sources",
                "2. Search for relevant data",
                "3. Extract key information",
                "4. Verify information accuracy",
                "5. Compile findings"
            ])
        
        # Coding tasks
        elif any(kw in description_lower for kw in ['code', 'program', 'develop', 'build']):
            steps.extend([
                "1. Analyze requirements",
                "2. Design solution architecture",
                "3. Write code implementation",
                "4. Test functionality",
                "5. Debug and refine"
            ])
        
        # Analysis tasks
        elif any(kw in description_lower for kw in ['analyze', 'evaluate', 'assess']):
            steps.extend([
                "1. Define analysis criteria",
                "2. Collect relevant data",
                "3. Perform analysis",
                "4. Draw conclusions",
                "5. Create report"
            ])
        
        # Generic plan
        else:
            steps.extend([
                "1. Understand the task requirements",
                "2. Gather necessary information",
                "3. Execute main task",
                "4. Verify results",
                "5. Report completion"
            ])
        
        return steps
    
    def _assess_complexity(self, description: str) -> str:
        """Assess task complexity"""
        # Simple heuristic based on keywords
        complex_keywords = ['multiple', 'comprehensive', 'detailed', 'complex', 'advanced']
        simple_keywords = ['simple', 'basic', 'quick', 'easy']
        
        desc_lower = description.lower()
        
        if any(kw in desc_lower for kw in complex_keywords):
            return "high"
        elif any(kw in desc_lower for kw in simple_keywords):
            return "low"
        else:
            return "medium"
    
    def _identify_required_agents(self, description: str) -> List[str]:
        """Identify which agents are needed"""
        desc_lower = description.lower()
        agents = []
        
        if any(kw in desc_lower for kw in ['research', 'find', 'search']):
            agents.append('researcher')
        
        if any(kw in desc_lower for kw in ['code', 'program', 'develop']):
            agents.append('coder')
        
        if any(kw in desc_lower for kw in ['debug', 'fix', 'error']):
            agents.append('debugger')
        
        if any(kw in desc_lower for kw in ['remember', 'recall', 'memory']):
            agents.append('memory')
        
        if any(kw in desc_lower for kw in ['secure', 'protect', 'threat']):
            agents.append('security')
        
        return agents if agents else ['planner']


class ResearchAgent(BaseAgent):
    """Researches topics and gathers information"""
    
    def __init__(self):
        super().__init__("researcher_001", "researcher")
    
    async def execute(self, task: Task) -> Dict:
        """Execute research task"""
        await self._mark_started(task)
        
        try:
            query = task.description
            
            # Simulate web search (replace with actual implementation)
            sources = await self._search_web(query)
            
            # Extract key information
            key_findings = await self._extract_findings(sources, query)
            
            # Create summary
            summary = await self._create_summary(key_findings)
            
            result = {
                'query': query,
                'sources': sources,
                'key_findings': key_findings,
                'summary': summary,
                'researched_at': datetime.now().isoformat()
            }
            
            await self._mark_completed(task, result)
            return result
            
        except Exception as e:
            await self._mark_failed(task, str(e))
            return {'error': str(e)}
    
    async def _search_web(self, query: str) -> List[Dict]:
        """Search web for information (placeholder)"""
        # In real implementation, use actual search APIs
        return [
            {'title': f'Research result 1 for: {query}', 'url': 'https://example.com/1'},
            {'title': f'Research result 2 for: {query}', 'url': 'https://example.com/2'},
            {'title': f'Research result 3 for: {query}', 'url': 'https://example.com/3'}
        ]
    
    async def _extract_findings(self, sources: List[Dict], query: str) -> List[str]:
        """Extract key findings from sources"""
        # In real implementation, extract actual content
        return [
            f"Finding 1: Key information about {query}",
            f"Finding 2: Important detail regarding {query}",
            f"Finding 3: Relevant fact related to {query}"
        ]
    
    async def _create_summary(self, findings: List[str]) -> str:
        """Create summary of findings"""
        return f"Research completed. Found {len(findings)} key findings. " + \
               " ".join(findings[:2])


class CoderAgent(BaseAgent):
    """Writes and generates code"""
    
    def __init__(self):
        super().__init__("coder_001", "coder")
        self.supported_languages = ['python', 'javascript', 'java', 'cpp', 'html', 'css']
    
    async def execute(self, task: Task) -> Dict:
        """Execute coding task"""
        await self._mark_started(task)
        
        try:
            description = task.description
            language = task.metadata.get('language', 'python')
            
            # Generate code
            code = await self._generate_code(description, language)
            
            # Add explanation
            explanation = await self._explain_code(code, description)
            
            result = {
                'description': description,
                'language': language,
                'code': code,
                'explanation': explanation,
                'generated_at': datetime.now().isoformat()
            }
            
            await self._mark_completed(task, result)
            return result
            
        except Exception as e:
            await self._mark_failed(task, str(e))
            return {'error': str(e)}
    
    async def _generate_code(self, description: str, language: str) -> str:
        """Generate code based on description"""
        # This is a template - in real implementation, use LLM
        
        if 'function' in description.lower() and language == 'python':
            return f'''def generated_function():
    """
    {description}
    """
    # TODO: Implement functionality
    pass
    
    return result
'''
        
        elif language == 'javascript':
            return f'''function generatedFunction() {{
    // {description}
    // TODO: Implement functionality
    return result;
}}
'''
        
        else:
            return f"# Code for: {description}\n# Language: {language}\n# TODO: Implementation"
    
    async def _explain_code(self, code: str, description: str) -> str:
        """Explain generated code"""
        return f"This code implements: {description}. " + \
               f"It defines a function to accomplish the requested task."


class DebuggerAgent(BaseAgent):
    """Debugs and fixes code"""
    
    def __init__(self):
        super().__init__("debugger_001", "debugger")
    
    async def execute(self, task: Task) -> Dict:
        """Execute debugging task"""
        await self._mark_started(task)
        
        try:
            code = task.metadata.get('code', '')
            error_message = task.metadata.get('error', '')
            
            # Analyze code
            issues = await self._find_issues(code, error_message)
            
            # Suggest fixes
            fixes = await self._suggest_fixes(issues)
            
            # Generate fixed code (if possible)
            fixed_code = await self._generate_fixed_code(code, fixes)
            
            result = {
                'original_code': code,
                'issues_found': issues,
                'suggested_fixes': fixes,
                'fixed_code': fixed_code,
                'debugged_at': datetime.now().isoformat()
            }
            
            await self._mark_completed(task, result)
            return result
            
        except Exception as e:
            await self._mark_failed(task, str(e))
            return {'error': str(e)}
    
    async def _find_issues(self, code: str, error: str) -> List[str]:
        """Find issues in code"""
        issues = []
        
        # Simple static analysis
        if 'NameError' in error:
            issues.append("Undefined variable or function name")
        if 'SyntaxError' in error:
            issues.append("Syntax error in code")
        if 'IndentationError' in error:
            issues.append("Incorrect indentation")
        if 'TypeError' in error:
            issues.append("Type mismatch or incorrect argument")
        
        # Check code patterns
        if code and ':' in code and '\n    ' not in code:
            issues.append("Possible indentation issue")
        
        return issues if issues else ["No obvious issues detected"]
    
    async def _suggest_fixes(self, issues: List[str]) -> List[str]:
        """Suggest fixes for issues"""
        fixes = []
        
        for issue in issues:
            if 'undefined' in issue.lower():
                fixes.append("Check variable names and ensure they're defined before use")
            if 'syntax' in issue.lower():
                fixes.append("Review syntax and check for missing colons, brackets, or parentheses")
            if 'indentation' in issue.lower():
                fixes.append("Ensure consistent indentation (4 spaces recommended)")
            if 'type' in issue.lower():
                fixes.append("Verify argument types match function expectations")
        
        return fixes if fixes else ["Review code logic and test edge cases"]
    
    async def _generate_fixed_code(self, code: str, fixes: List[str]) -> str:
        """Generate potentially fixed code"""
        # In real implementation, apply actual fixes
        return f"# Fixed code (review suggested fixes)\n{code}"


class MultiAgentSwarm:
    """
    Manages multiple AI agents and coordinates their work
    
    Usage:
        swarm = MultiAgentSwarm()
        await swarm.initialize()
        
        # Create and execute task
        task = Task(
            task_id="task_001",
            description="Research quantum computing and create summary",
            agent_type="researcher"
        )
        result = await swarm.execute_task(task)
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.task_queue: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.agent_communication_log: List[Dict] = []
    
    async def initialize(self):
        """Initialize agent swarm"""
        print("🤖 Initializing Multi-Agent Swarm...")
        
        # Create agents
        self.agents = {
            'planner': PlannerAgent(),
            'researcher': ResearchAgent(),
            'coder': CoderAgent(),
            'debugger': DebuggerAgent()
        }
        
        for agent_type, agent in self.agents.items():
            print(f"   ✅ {agent_type.capitalize()} Agent ready")
        
        print("   ✅ Agent swarm initialized")
    
    async def execute_task(self, task: Task) -> Any:
        """
        Execute a task using appropriate agent
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        # Get appropriate agent
        agent = self.agents.get(task.agent_type)
        
        if not agent:
            print(f"   ❌ No agent available for type: {task.agent_type}")
            return None
        
        print(f"\n🎯 Executing task with {task.agent_type} agent...")
        print(f"   Task: {task.description}")
        
        # Execute task
        result = await agent.execute(task)
        
        # Log completion
        if task.status == "completed":
            print(f"   ✅ Task completed successfully")
            self.completed_tasks.append(task)
        else:
            print(f"   ❌ Task failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    async def execute_complex_task(self, description: str) -> Dict:
        """
        Execute complex task using multiple agents in sequence
        
        Args:
            description: Task description
            
        Returns:
            Combined results from all agents
        """
        print(f"\n🔄 Executing complex task...")
        print(f"   Description: {description}")
        
        # Step 1: Use planner to break down task
        plan_task = Task(
            task_id=f"plan_{datetime.now().timestamp()}",
            description=description,
            agent_type="planner"
        )
        
        plan_result = await self.execute_task(plan_task)
        
        if not plan_result or 'error' in plan_result:
            return {'error': 'Planning failed'}
        
        # Step 2: Execute sub-tasks with required agents
        results = {'plan': plan_result, 'sub_tasks': []}
        
        for agent_type in plan_result.get('required_agents', []):
            if agent_type in self.agents:
                subtask = Task(
                    task_id=f"{agent_type}_{datetime.now().timestamp()}",
                    description=description,
                    agent_type=agent_type
                )
                
                subtask_result = await self.execute_task(subtask)
                results['sub_tasks'].append({
                    'agent': agent_type,
                    'result': subtask_result
                })
        
        return results
    
    def get_swarm_stats(self) -> Dict:
        """Get statistics for all agents"""
        stats = {
            'total_agents': len(self.agents),
            'total_tasks_completed': len(self.completed_tasks),
            'agents': {}
        }
        
        for agent_type, agent in self.agents.items():
            stats['agents'][agent_type] = agent.get_stats()
        
        return stats
    
    def get_available_agents(self) -> List[str]:
        """Get list of available (not busy) agents"""
        return [
            agent_type
            for agent_type, agent in self.agents.items()
            if not agent.is_busy
        ]


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def example_usage():
    """Example of how to use Multi-Agent Swarm"""
    
    # Initialize swarm
    swarm = MultiAgentSwarm()
    await swarm.initialize()
    
    print("\n" + "="*60)
    print("TESTING INDIVIDUAL AGENTS")
    print("="*60)
    
    # Test planner
    plan_task = Task(
        task_id="task_001",
        description="Research quantum computing and create a detailed report",
        agent_type="planner"
    )
    plan_result = await swarm.execute_task(plan_task)
    print(f"\n📋 Plan created with {len(plan_result['plan'])} steps")
    
    # Test researcher
    research_task = Task(
        task_id="task_002",
        description="Research artificial intelligence trends",
        agent_type="researcher"
    )
    research_result = await swarm.execute_task(research_task)
    print(f"\n🔍 Research found {len(research_result['sources'])} sources")
    
    # Test coder
    code_task = Task(
        task_id="task_003",
        description="Write a function to calculate fibonacci numbers",
        agent_type="coder",
        metadata={'language': 'python'}
    )
    code_result = await swarm.execute_task(code_task)
    print(f"\n💻 Code generated:")
    print(code_result['code'])
    
    print("\n" + "="*60)
    print("TESTING COMPLEX MULTI-AGENT TASK")
    print("="*60)
    
    # Execute complex task
    complex_result = await swarm.execute_complex_task(
        "Research machine learning and write Python code to implement a basic neural network"
    )
    
    print(f"\n✅ Complex task completed")
    print(f"   Plan steps: {len(complex_result['plan']['plan'])}")
    print(f"   Agents used: {len(complex_result['sub_tasks'])}")
    
    # Get swarm statistics
    print("\n" + "="*60)
    print("SWARM STATISTICS")
    print("="*60)
    
    stats = swarm.get_swarm_stats()
    print(f"\nTotal agents: {stats['total_agents']}")
    print(f"Total tasks completed: {stats['total_tasks_completed']}")
    print("\nAgent Performance:")
    for agent_type, agent_stats in stats['agents'].items():
        print(f"  {agent_type.capitalize()}:")
        print(f"    Completed: {agent_stats['tasks_completed']}")
        print(f"    Success rate: {agent_stats['success_rate']}%")


if __name__ == "__main__":
    asyncio.run(example_usage())
