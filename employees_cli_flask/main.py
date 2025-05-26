from app.service.employee_service import get_all_employees, get_bench_employees, get_by_project_status,get_employees_between_salary_range
from app.service.employee_service import get_employees_by_department,get_employees_by_designation,get_employees_by_location,get_employees_above_threshold_age,get_employees_between_age_limit, get_employees_undre_project
from flask import Flask, jsonify, request
from app.util.logger import get_logger
from app.util.decoraters import handle_exceptions, time_execution_logger

# Initialize logger with application name
logger = get_logger('employee_api.main')

app = Flask(__name__)

@app.route("/")
def index():
    logger.info(f"API REQUEST: Health check requested from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    return {"Status" : "Employee API is Running as Expected. State = Healthy"}

@app.route("/employees", methods=["GET"])
@time_execution_logger
@handle_exceptions
def all_employees(): # List All Employees
    employees = get_all_employees()
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/bench", methods=["GET"])
def bench_employees(): # Find All Employees On Bench
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Bench employees endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_bench_employees()
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} bench employees with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/active_projects", methods=["GET"])
def active_projects(): # Find All Employees With Active Projects
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Active projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_by_project_status("active")
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees with active projects with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/completed_projects", methods=["GET"])
def completed_projects(): # Find All Employees With Completed Projects
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: Completed projects endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees = get_by_project_status("completed")
    
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees with completed projects with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/by_department/<department>", methods=["GET"])
#getting the employes by specified department
def emoloyees_by_department(department):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees by department endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_by_department(department)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees by department with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/by_designation/<designation>", methods=["GET"])
#getting the employees by specified designation
def employees_by_designation(designation):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees by designation endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_by_designation(designation)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees by designation with HTTP 200 status")
    return jsonify(employees), 200


@time_execution_logger
@app.route("/employees/by_location/<location>", methods=["GET"])
#getting the employees by specified location
def employess_by_location(location):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees by location endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_by_location(location)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees by location with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/by_salary_range/<min_salary>/<max_salary>", methods=["GET"])
#getting the employees by specified salary range
def employess_by_salary_range(min_salary,max_salary):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees by salary range endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_between_salary_range(min_salary,max_salary)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees between specified salary range with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/by_threshold_age/<age>", methods=["GET"])
#getting the employees by above specified threshold age
def employess_above_age(age):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees by above threshold age endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees=get_employees_above_threshold_age(age)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees by above threshold age with HTTP 200 status")
    return jsonify(employees), 200

@time_execution_logger
@app.route("/employees/by_age_limits/<lower_age_limit>/<upper_age_limit>", methods=["GET"])
#getting the employees between age limits
def employess_between_age_limit(lower_age_limit,upper_age_limit):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees between age limits endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_between_age_limit(lower_age_limit,upper_age_limit)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees between age limitwith HTTP 200 status")
    return jsonify(employees), 200

time_execution_logger
@app.route("/employees/by_project/<project_name>", methods=["GET"])
#getting the employees under the specified project
def employess_under_project(project_name):
    request_id = id(request)
    logger.info(f"API REQUEST [{request_id}]: employees under tghe project endpoint called from IP: {request.remote_addr}, User-Agent: {request.headers.get('User-Agent', 'Unknown')}")
    
    employees= get_employees_undre_project(project_name)
    logger.info(f"API RESPONSE [{request_id}]: Returning {len(employees)} employees under specified project with HTTP 200 status")
    return jsonify(employees), 200








if __name__ == "__main__":
    logger.info("SERVER STARTUP: Initializing Employee API server")
    logger.info(f"SERVER CONFIG: Debug mode: {app.debug}, Host: 127.0.0.1, Port: 5000")
    
    # Register available endpoints for logging
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(f"{rule.endpoint} [{', '.join(rule.methods)}] {rule}")
    
    logger.info(f"SERVER ROUTES: Available endpoints: {routes}")
    logger.info("SERVER READY: Employee API server is ready to accept requests")
    
    app.run(debug=True)
    print(app.url_map)