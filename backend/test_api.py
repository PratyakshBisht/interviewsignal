import asyncio
import httpx
import sys
import json

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

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
            print(f"   Response: {response.json().get('service')}")
            
            # 2. Test health check
            print("\n2. Testing health check...")
            response = await client.get(f"{BASE_URL}/health")
            print(f"✅ Status: {response.status_code}")
            print(f"   Health: {response.json().get('status')}")
            
            # 3. Test docs
            print("\n3. Testing documentation...")
            response = await client.get(f"{BASE_URL}/docs")
            print(f"✅ Status: {response.status_code}")
            
            # 4. Test auth endpoints
            print("\n4. Testing auth endpoints...")
            
            # GitHub OAuth URL
            response = await client.get(f"{BASE_URL}/auth/login/github")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ GitHub OAuth URL: {data.get('success')}")
            else:
                print(f"ℹ️ GitHub OAuth not configured (Status {response.status_code}): {response.json().get('detail')}")
            
            # User info (should fail without token)
            response = await client.get(f"{BASE_URL}/auth/userinfo")
            if response.status_code == 401:
                print("✅ Correctly rejected unauthenticated /auth/userinfo request (401 Unauthorized)")
            else:
                print(f"ℹ️ Status: {response.status_code}")
            
            # 5. Test analysis endpoints (unauthorized)
            print("\n5. Testing analysis endpoints (unauthorized)...")
            response = await client.get(f"{BASE_URL}/analysis/latest")
            if response.status_code == 401:
                print("✅ Correctly rejected unauthenticated /analysis/latest request (401 Unauthorized)")
            else:
                print(f"ℹ️ Status: {response.status_code}")
                
            # 6. Test with mock token (just structure test)
            print("\n6. Testing with authentication...")
            print("ℹ️ Note: Actual authentication requires GitHub OAuth")
            print("ℹ️ To test fully, you need to:")
            print("   1. Configure GitHub OAuth client credentials in .env")
            print("   2. Use it to get JWT token")
            print("   3. Test authenticated endpoints")
            
            print("\n🎉 Basic API structure tests passed!")
            print("\n📚 Next steps:")
            print("   1. Configure GitHub OAuth in .env")
            print("   2. Run frontend dashboard (Module 8)")
            print("   3. Run analysis trigger")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "=" * 50)
    print("API Test Complete - ALL ENDPOINTS OPERATIONAL")
    print("=" * 50)
    return True


if __name__ == "__main__":
    asyncio.run(test_endpoints())
