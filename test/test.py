import sys
import os

# Add the src directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that basic modules can be imported"""
    try:
        # Test core modules
        from agent import BudgetBuddyAgent
        from components.utils.storage import get_profile, get_all_months_data
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_agent_creation():
    """Test that agent can be created (mocked)"""
    try:
        # Mock AWS dependencies to avoid actual API calls
        import unittest.mock as mock
        
        with mock.patch('agent.boto3.Session') as mock_session, \
             mock.patch('agent.BedrockModel') as mock_provider:
            
            # Setup mocks
            mock_client = mock.Mock()
            mock_session.return_value.client.return_value = mock_client
            mock_provider.return_value = mock.Mock()
            
            from agent import BudgetBuddyAgent
            agent = BudgetBuddyAgent()
            
            assert agent is not None, "Agent should be created"
            assert hasattr(agent, 'run'), "Agent should have run method"
            
            print("✅ Agent creation successful")
            return True
            
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def run_all_tests():
    """Run all simple tests"""
    print("🚀 Running simple tests...")
    print("-" * 40)
    
    tests = [
        test_imports,
        test_agent_creation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)
    
    print("-" * 40)
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed")
        return False

if __name__ == "__main__":
    # Run tests when file is executed directly
    success = run_all_tests()
    sys.exit(0 if success else 1)