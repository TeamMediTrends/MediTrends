import psycopg2
import json

def get_longitudinal_trends(patient_id, test_type, start_date=None, end_date=None):
    """Fetch test results over time for a given patient and test type."""
    try:
        conn = psycopg2.connect(
            dbname='your_database', user='your_user', password='your_password', host='your_host'
        )
        cur = conn.cursor()

        query = """
            SELECT test_date, result_value
            FROM test_results
            WHERE patient_id = %s AND test_type = %s
        """
        params = [patient_id, test_type]

        if start_date and end_date:
            query += " AND test_date BETWEEN %s AND %s"
            params.extend([start_date, end_date])
        
        query += " ORDER BY test_date"
        
        cur.execute(query, params)
        results = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return json.dumps([{"date": row[0].strftime('%Y-%m-%d'), "value": row[1]} for row in results])
    
    except Exception as e:
        return json.dumps({"error": str(e)})

# Example usage:
# print(get_longitudinal_trends(123, 'Blood Glucose', '2020-01-01', '2025-01-01'))
