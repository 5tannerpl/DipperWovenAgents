curl -s -X POST   http://localhost:8000/api/agent/invoke   -H "Content-Type: application/json"   -d '{
    "case_id": "12345",
    "target_type": "note",
    "content": "Customer says his solicitor will manage the account. Collector plans to call the customer tomorrow for payment.",
    "jurisdiction": "AU",
    "region": "AU"
  }' | jq .

  