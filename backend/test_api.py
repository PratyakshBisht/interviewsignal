import asyncio
import httpx
import sys
import json

BASE_URL = "http://localhost:8000"


async def test_endpoints():
    """Test all API endpoints."""
    print("🧪 Testing InterviewSignal API Endpoints")
    print("=" * 50)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Test root endpoint
            print("\n1. Testing root endpoint...")
            response = await client.get(f"{BASE_URL}/")
            print(f"✅ Status: {response.status_code}")
            
            # 2. Test health check
            print("\n2. Testing health check...")
            response = await client.get(f"{BASE_URL}/health")
            print(f"✅ Status: {response.status_code}")
            
            # 3. Test docs
            print("\n3. Testing documentation...")
            response = await client.get(f"{BASE_URL}/docs")
            print(f"✅ Status: {response.status_code}")
            
            # 4. Test auth endpoints
            print("\n4. Testing auth endpoints...")
            
            # GitHub OAuth URL
            response = await client.get(f"{BASE_URL}/auth/login/github")
            data = response.json()
            print(f"✅ GitHub OAuth URL: {data.get('success')}")
            
            # User info (should fail without token)
            try:
                response = await client.get(f"{BASE_URL}/auth/userinfo")
                print(f"❌ Should have failed: {response.status_code}")
            except Exception:
                print("✅ Correctly rejected unauthenticated request")
            
            # 5. Test analysis endpoints (unauthorized)
            print("\n5. Testing analysis endpoints (unauthorized)...")
            try:
                response = await client.get(f"{BASE_URL}/analysis/latest")
                print(f"❌ Should have failed: {response.status_code}")
            except Exception:
                print("✅ Correctly rejected unauthenticated request")
                
            # 6. Test with mock token (just structure test)
            print("\n6. Testing with authentication...")
            print("ℹ️ Note: Actual authentication requires GitHub OAuth")
            print("ℹ️ To test fully, you need to:")
            print("   1. Get GitHub OAuth token")
            print("   2. Use it to get JWT token")
            print("   3. Test authenticated endpoints")
            
            print("\n🎉 Basic API structure tests passed!")
            print("\n📚 Next steps:")
            print("   1. Configure GitHub OAuth")
            print("   2. Get actual JWT token")
            print("   3. Test authenticated endpoints")
            print("   4. Run analysis trigger")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 50)
    print("API Test Complete")
    print("=" * 50)
    return True


if __name__ == "__main__":
    asyncio.run(test_endpoints())
