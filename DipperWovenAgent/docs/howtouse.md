重启服务
pkill -f uvicorn

然后：

uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload


  phase-1 tests
  1.
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "12345",
    "target_type": "note",
    "content": "Customer says his solicitor will manage the account. Collector plans to call the customer tomorrow for payment.",
    "jurisdiction": "AU",
    "region": "AU"
  }' | jq .

  1- 
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "2",
    "content": "Customer has lost his job and says he cannot afford the current repayment arrangement."
  }' | jq .

  3-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "3",
    "content": "Customer disputes the outstanding balance and says the amount is incorrect."
  }' | jq .

  4-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "4",
    "content": "Called customer. Customer promised to pay $500 next Friday."
  }' | jq .
  
  5-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "5",
    "content": "Customer confirmed their mailing address and requested a copy of the latest statement."
  }' | jq .

  6-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "6",
    "content": "Customer says the collector was rude during the previous call and wants to make a formal complaint about how the account has been handled."
  }' | jq .

  7-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "7",
    "content": "Customer says he was declared bankrupt last month and that a trustee is now managing his financial affairs."
  }' | jq .

  8-
  curl -s -X POST \
  http://localhost:8000/api/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "5b",
    "content": "Customer requested a copy of the latest statement. Collector will email the statement to the customer tomorrow."
  }' | jq .