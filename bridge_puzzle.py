from experta import *
from collections import deque
import time

# Person crossing times
CROSSING_TIMES = {
    'You': 1,
    'LabAssistant': 2,
    'Worker': 5,
    'Scientist': 10
}

TIME_LIMIT = 17

class TrueDFS:
    """True DFS implementation without using experta's salience system"""
    
    def __init__(self):
        self.visited_states = set()
        self.states_explored = []
        self.solution_found = False
        self.solution_path = None
        self.solution_time = None
        self.tree_structure = {}  # For building the tree
        
    def solve(self):
        """Solve using true DFS with stack"""
        # Stack for DFS: (left, right, flashlight_side, time, path, depth, parent_id)
        initial_state = ({'You', 'LabAssistant', 'Worker', 'Scientist'}, 
                        set(), 'left', 0, [], 0, None)
        
        stack = [initial_state]
        state_id = 0
        
        while stack and not self.solution_found:
            left, right, flashlight_side, time, path, depth, parent_id = stack.pop()
            
            # Create state key for visited check
            state_key = (frozenset(left), frozenset(right), flashlight_side, time)
            
            if state_key in self.visited_states:
                continue
                
            self.visited_states.add(state_key)
            
            current_id = state_id
            state_id += 1
            
            # Track exploration with tree structure
            state_info = {
                'id': current_id,
                'left': set(left),
                'right': set(right),
                'flashlight_side': flashlight_side,
                'time': time,
                'depth': depth,
                'action': self.get_action_from_path(path),
                'order': len(self.states_explored),
                'parent_id': parent_id,
                'children': [],
                'is_solution': False
            }
            
            # Add to tree structure
            self.tree_structure[current_id] = state_info
            if parent_id is not None:
                self.tree_structure[parent_id]['children'].append(current_id)
            
            self.states_explored.append(state_info)
            
            # Check if goal reached
            if len(left) == 0:
                self.solution_found = True
                self.solution_path = path
                self.solution_time = time
                state_info['is_solution'] = True
                self.mark_solution_path(current_id)
                return True
            
            # Generate next states (DFS explores in reverse order due to stack)
            next_states = []
            
            if flashlight_side == 'left':
                # People crossing from left to right
                people_list = list(left)
                for i in range(len(people_list)):
                    for j in range(i + 1, len(people_list)):
                        person1, person2 = people_list[i], people_list[j]
                        crossing_time = max(CROSSING_TIMES[person1], CROSSING_TIMES[person2])
                        new_time = time + crossing_time
                        
                        if new_time <= TIME_LIMIT:
                            new_left = left - {person1, person2}
                            new_right = right | {person1, person2}
                            new_path = path + [(person1, person2, 'cross', crossing_time)]
                            
                            next_states.append((new_left, new_right, 'right', new_time, new_path, depth + 1, current_id))
            
            else:  # flashlight_side == 'right'
                # People returning from right to left
                for person in right:
                    crossing_time = CROSSING_TIMES[person]
                    new_time = time + crossing_time
                    
                    if new_time <= TIME_LIMIT:
                        new_left = left | {person}
                        new_right = right - {person}
                        new_path = path + [(person, 'return', crossing_time)]
                        
                        next_states.append((new_left, new_right, 'left', new_time, new_path, depth + 1, current_id))
            
            # Add states to stack in reverse order for proper DFS behavior
            for state in reversed(next_states):
                stack.append(state)
        
        return False
    
    def mark_solution_path(self, solution_id):
        """Mark all nodes in the solution path"""
        current_id = solution_id
        while current_id is not None:
            self.tree_structure[current_id]['is_solution'] = True
            current_id = self.tree_structure[current_id]['parent_id']
    
    def get_action_from_path(self, path):
        """Get the last action from path for display"""
        if not path:
            return "Initial state"
        
        last_step = path[-1]
        if len(last_step) == 3:  # Return step
            return f"{last_step[0]} returns ({last_step[2]}min)"
        else:  # Cross step
            return f"{last_step[0]} & {last_step[1]} cross ({last_step[3]}min)"

class TrueBFS:
    """True BFS implementation without using experta's salience system"""
    
    def __init__(self):
        self.visited_states = set()
        self.states_explored = []
        self.solution_found = False
        self.solution_path = None
        self.solution_time = None
        self.tree_structure = {}  # For building the tree
        
    def solve(self):
        """Solve using true BFS with queue"""
        # Queue for BFS: (left, right, flashlight_side, time, path, depth, parent_id)
        initial_state = ({'You', 'LabAssistant', 'Worker', 'Scientist'}, 
                        set(), 'left', 0, [], 0, None)
        
        queue = deque([initial_state])
        state_id = 0
        
        while queue and not self.solution_found:
            left, right, flashlight_side, time, path, depth, parent_id = queue.popleft()
            
            # Create state key for visited check
            state_key = (frozenset(left), frozenset(right), flashlight_side, time)
            
            if state_key in self.visited_states:
                continue
                
            self.visited_states.add(state_key)
            
            current_id = state_id
            state_id += 1
            
            # Track exploration with tree structure
            state_info = {
                'id': current_id,
                'left': set(left),
                'right': set(right),
                'flashlight_side': flashlight_side,
                'time': time,
                'depth': depth,
                'action': self.get_action_from_path(path),
                'order': len(self.states_explored),
                'parent_id': parent_id,
                'children': [],
                'is_solution': False
            }
            
            # Add to tree structure
            self.tree_structure[current_id] = state_info
            if parent_id is not None:
                self.tree_structure[parent_id]['children'].append(current_id)
            
            self.states_explored.append(state_info)
            
            # Check if goal reached
            if len(left) == 0:
                self.solution_found = True
                self.solution_path = path
                self.solution_time = time
                state_info['is_solution'] = True
                self.mark_solution_path(current_id)
                return True
            
            # Generate next states (BFS explores in order)
            if flashlight_side == 'left':
                # People crossing from left to right
                people_list = list(left)
                for i in range(len(people_list)):
                    for j in range(i + 1, len(people_list)):
                        person1, person2 = people_list[i], people_list[j]
                        crossing_time = max(CROSSING_TIMES[person1], CROSSING_TIMES[person2])
                        new_time = time + crossing_time
                        
                        if new_time <= TIME_LIMIT:
                            new_left = left - {person1, person2}
                            new_right = right | {person1, person2}
                            new_path = path + [(person1, person2, 'cross', crossing_time)]
                            
                            queue.append((new_left, new_right, 'right', new_time, new_path, depth + 1, current_id))
            
            else:  # flashlight_side == 'right'
                # People returning from right to left
                for person in right:
                    crossing_time = CROSSING_TIMES[person]
                    new_time = time + crossing_time
                    
                    if new_time <= TIME_LIMIT:
                        new_left = left | {person}
                        new_right = right - {person}
                        new_path = path + [(person, 'return', crossing_time)]
                        
                        queue.append((new_left, new_right, 'left', new_time, new_path, depth + 1, current_id))
        
        return False
    
    def mark_solution_path(self, solution_id):
        """Mark all nodes in the solution path"""
        current_id = solution_id
        while current_id is not None:
            self.tree_structure[current_id]['is_solution'] = True
            current_id = self.tree_structure[current_id]['parent_id']
    
    def get_action_from_path(self, path):
        """Get the last action from path for display"""
        if not path:
            return "Initial state"
        
        last_step = path[-1]
        if len(last_step) == 3:  # Return step
            return f"{last_step[0]} returns ({last_step[2]}min)"
        else:  # Cross step
            return f"{last_step[0]} & {last_step[1]} cross ({last_step[3]}min)"

def print_solution_tree(solver, algorithm_name):
    """Print the solution tree for the algorithm"""
    print(f"\n🌳 {algorithm_name} SOLUTION TREE")
    print("=" * 60)
    
    if not solver.tree_structure:
        print("No tree structure available")
        return
    
    # Find root node (parent_id is None)
    root_id = None
    for node_id, node_info in solver.tree_structure.items():
        if node_info['parent_id'] is None:
            root_id = node_id
            break
    
    if root_id is None:
        print("No root node found")
        return
    
    def print_node(node_id, prefix="", is_last=True):
        """Recursively print the tree structure"""
        if node_id not in solver.tree_structure:
            return
        
        node = solver.tree_structure[node_id]
        
        # Choose connector based on position
        connector = "└── " if is_last else "├── "
        
        # Format the node display
        left_str = "{" + ", ".join(sorted(node['left'])) + "}"
        right_str = "{" + ", ".join(sorted(node['right'])) + "}"
        
        # Color coding for solution path
        if node['is_solution']:
            node_marker = "🟢"  # Green for solution path
        else:
            node_marker = "🔴"  # Red for explored but not solution
        
        print(f"{prefix}{connector}{node_marker} [{node['id']}] {node['action']}")
        print(f"{prefix}{'    ' if is_last else '│   '}    L: {left_str}")
        print(f"{prefix}{'    ' if is_last else '│   '}    R: {right_str}")
        print(f"{prefix}{'    ' if is_last else '│   '}    Time: {node['time']}min, Flash: {node['flashlight_side']}")
        
        # Print children
        children = node['children']
        for i, child_id in enumerate(children):
            is_last_child = (i == len(children) - 1)
            new_prefix = prefix + ("    " if is_last else "│   ")
            print_node(child_id, new_prefix, is_last_child)
    
    print_node(root_id)
    
    # Print legend
    print("\n📖 Legend:")
    print("🟢 Solution path node")
    print("🔴 Explored node (not in solution)")
    print("L: Left side, R: Right side")
    print("Flash: Flashlight location")

def print_solution(algorithm_name, solver):
    """Print the solution found by the algorithm"""
    if solver.solution_found:
        print(f"🎯 {algorithm_name} Solution Found!")
        print(f"⏱️  Total Time: {solver.solution_time} minutes")
        print("📋 Solution Path:")
        for i, step in enumerate(solver.solution_path, 1):
            if len(step) == 3:  # Return step
                print(f"   {i}. {step[0]} returns ⬅️ (Time: {step[2]} min)")
            else:  # Cross step
                print(f"   {i}. {step[0]} and {step[1]} cross ➡️ (Time: {step[3]} min)")
    else:
        print(f"❌ {algorithm_name}: No solution found within time limit")
    print()

def print_exploration_comparison(dfs_solver, bfs_solver):
    """Compare the exploration patterns of DFS and BFS"""
    print("🔍 EXPLORATION PATTERN COMPARISON")
    print("=" * 60)
    
    print(f"📊 DFS States Explored: {len(dfs_solver.states_explored)}")
    print(f"📊 BFS States Explored: {len(bfs_solver.states_explored)}")
    print()
    
    print("🌳 First 10 States Explored:")
    print("DFS Order vs BFS Order")
    print("-" * 40)
    
    max_show = min(10, len(dfs_solver.states_explored), len(bfs_solver.states_explored))
    
    for i in range(max_show):
        dfs_state = dfs_solver.states_explored[i]
        bfs_state = bfs_solver.states_explored[i]
        
        print(f"Step {i+1}:")
        print(f"  DFS: Depth {dfs_state['depth']} - {dfs_state['action']}")
        print(f"  BFS: Depth {bfs_state['depth']} - {bfs_state['action']}")
        print()
    
    # Show depth distribution
    print("📈 Depth Distribution:")
    
    # Count states by depth for DFS
    dfs_depth_count = {}
    for state in dfs_solver.states_explored:
        depth = state['depth']
        dfs_depth_count[depth] = dfs_depth_count.get(depth, 0) + 1
    
    # Count states by depth for BFS
    bfs_depth_count = {}
    for state in bfs_solver.states_explored:
        depth = state['depth']
        bfs_depth_count[depth] = bfs_depth_count.get(depth, 0) + 1
    
    all_depths = sorted(set(dfs_depth_count.keys()) | set(bfs_depth_count.keys()))
    
    for depth in all_depths:
        dfs_count = dfs_depth_count.get(depth, 0)
        bfs_count = bfs_depth_count.get(depth, 0)
        print(f"  Depth {depth}: DFS={dfs_count}, BFS={bfs_count}")

def main():
    print("=" * 70)
    print("🌉           TRUE DFS vs BFS COMPARISON           🔦")
    print("=" * 70)
    
    # Solve with DFS
    print("🔍 SOLVING WITH TRUE DEPTH-FIRST SEARCH")
    print("-" * 50)
    dfs_solver = TrueDFS()
    start_time = time.time()
    dfs_result = dfs_solver.solve()
    dfs_time = time.time() - start_time
    print(f"⏱️  DFS Execution Time: {dfs_time:.4f} seconds")
    print_solution("DFS", dfs_solver)
    
    # Solve with BFS
    print("🔍 SOLVING WITH TRUE BREADTH-FIRST SEARCH")
    print("-" * 50)
    bfs_solver = TrueBFS()
    start_time = time.time()
    bfs_result = bfs_solver.solve()
    bfs_time = time.time() - start_time
    print(f"⏱️  BFS Execution Time: {bfs_time:.4f} seconds")
    print_solution("BFS", bfs_solver)
    
    # Print solution trees
    print_solution_tree(dfs_solver, "DFS")
    print_solution_tree(bfs_solver, "BFS")
    
    # Compare results
    print_exploration_comparison(dfs_solver, bfs_solver)
    
    print("\n🔬 ALGORITHM ANALYSIS")
    print("=" * 50)
    print("📊 Key Observations:")
    
    if dfs_solver.solution_found and bfs_solver.solution_found:
        if dfs_solver.solution_time == bfs_solver.solution_time:
            print("✅ Both algorithms found optimal solutions with same time")
        elif dfs_solver.solution_time < bfs_solver.solution_time:
            print("⚠️  DFS found a better solution (less time)")
        else:
            print("✅ BFS found a better solution (less time)")
    
    print(f"• DFS explored {len(dfs_solver.states_explored)} states")
    print(f"• BFS explored {len(bfs_solver.states_explored)} states")
    print(f"• DFS execution time: {dfs_time:.4f}s")
    print(f"• BFS execution time: {bfs_time:.4f}s")
    
    print("\n💡 Expected Behavior:")
    print("• DFS: Goes deep first, may find suboptimal solutions quickly")
    print("• BFS: Explores level by level, guarantees shortest path")
    print("• BFS typically explores more states but finds optimal solution")
    print("• DFS uses less memory but may not find optimal solution")

if __name__ == "__main__":
    main()