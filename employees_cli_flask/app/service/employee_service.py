import json
from app.model.employee import Employee
from app.util.decoraters import handle_exceptions
from app.util.logger import get_logger

# Initialize logger
logger = get_logger(__name__)

EMPLOYEE_DATA_FILE = "app/data/employees_details.json"

@handle_exceptions
def load_employees():
    logger.info(f"INITIALIZATION: Starting to load employee data from file: {EMPLOYEE_DATA_FILE}")
    try:
        with open (EMPLOYEE_DATA_FILE, 'r') as f:
            employees_data = json.load(f)
            logger.info(f"DATA LOAD: Successfully read {len(employees_data)} employee records from JSON file")
            
            # Log sample of first employee record (with sensitive fields masked)
            if employees_data:
                sample = employees_data[0].copy()
                if 'salary' in sample:
                    sample['salary'] = '******'
                if 'dob' in sample:
                    sample['dob'] = '****-**-**'
                logger.info(f"DATA SAMPLE: First record structure: {sample}")
            
            employees = [Employee(**emp) for emp in employees_data]
            
            # Log departments statistics
            if employees:
                departments = {}
                for emp in employees:
                    dept = emp.department
                    departments[dept] = departments.get(dept, 0) + 1
                logger.info(f"STATISTICS: Department distribution: {departments}")
                
            logger.info(f"INITIALIZATION COMPLETE: Created {len(employees)} Employee objects successfully")
            return employees
    except Exception as e:
        logger.error(f"INITIALIZATION ERROR: Failed to load employees: {str(e)}")
        raise

employees = load_employees()

def get_all_employees():
    logger.info(f"API REQUEST: Retrieving complete employee dataset containing {len(employees)} records")
    result = [emp.to_dict() for emp in employees]
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with {sum(len(emp.get('projects', [])) for emp in result)} total projects")
    return result

def get_bench_employees():
    logger.info(f"API REQUEST: Filtering for bench employees from total {len(employees)} employees")
    bench_employees = list(filter(lambda e: e.is_on_bench(), employees))
    result = [emp.to_dict() for emp in bench_employees]
    
    # Calculate percentage of workforce on bench
    bench_percentage = (len(bench_employees) / len(employees)) * 100 if employees else 0
    
    logger.info(f"STATISTICS: Found {len(bench_employees)} employees on bench ({bench_percentage:.2f}% of workforce)")
    
    # Log department-wise bench distribution if bench employees exist
    if bench_employees:
        departments = {}
        for emp in bench_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"DETAILED BREAKDOWN: Bench employees by department: {departments}")
        
    logger.info(f"API RESPONSE: Returning {len(result)} bench employee records")
    return result

def get_by_project_status(status):
    """ Gets the list of all the Employees with their Projects as per the 
    status provided.

    Args:
        status (str):
    
    """
    logger.info(f"API REQUEST: Filtering employees by project status: '{status}'")
    filtered_employees = [emp for emp in employees if emp.has_project_with_status(status)]
    result = [emp.to_dict() for emp in filtered_employees]
    
    # Calculate percentage of workforce with this project status
    status_percentage = (len(filtered_employees) / len(employees)) * 100 if employees else 0
    
    # Count total projects with this status
    project_count = 0
    for emp in filtered_employees:
        for proj in emp.projects:
            if proj.status == status:
                project_count += 1
    
    # Log detailed statistics
    logger.info(f"STATISTICS: Found {len(filtered_employees)} employees ({status_percentage:.2f}% of workforce) with {project_count} '{status}' projects")
    
    # Log department-wise distribution if employees exist
    if filtered_employees:
        departments = {}
        for emp in filtered_employees:
            dept = emp.department
            departments[dept] = departments.get(dept, 0) + 1
        logger.info(f"DETAILED BREAKDOWN: Employees with '{status}' projects by department: {departments}")
    
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with '{status}' projects")
    return result

 #Gets the list of all the Employees with specified department.
def get_employees_by_department(department):
    
    logger.info(f"API REQUEST: Filtering of employees by department from total {len(employees)} employees")
    
    filtered_employees = [emp for emp in employees if emp.department.lower()== department.lower()]
    
    result = [emp.to_dict() for emp in filtered_employees]
    
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with specified department '{department}' projects")
    
    return result


 #Gets the list of all the Employees with specified designation.
def get_employees_by_designation(designation):
    
    logger.info(f"API REQUEST: Filtering of employees by designation from total {len(employees)} employees")
    
    filtered_employees = [emp for emp in employees if emp.designation.lower()== designation.lower()]
    
    result = [emp.to_dict() for emp in filtered_employees]
    
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with specified designation '{designation}' projects")
    
    return result

 #Gets the list of all the Employees with specified location.
def get_employees_by_location(location):

    logger.info(f"API REQUEST: Filtering of employees by location specified from total {len(employees)} employees")
    
    filtered_employees = [emp for emp in employees if emp.location.lower()== location.lower()]
    
    result = [emp.to_dict() for emp in filtered_employees]
    
    logger.info(f"API RESPONSE: Returning {len(result)} employee records with specified location '{location}' projects")
    
    return result


#sgetting the employees in between slary range
def get_employees_between_salary_range(min_salary,max_salary):
     
    min_salary=int(min_salary)
    max_salary=int(max_salary)
     
    logger.info(f"API REQUEST: Filtering of employees based on salary range from total {len(employees)} employees")

    filtered_employees=[emp for emp in employees if min_salary<=emp.salary<=max_salary]  
     
    result = [emp.to_dict() for emp in filtered_employees]

    logger.info(f"API RESPONSE: Returning {len(result)} employee records with specified salary range '{min_salary}' and '{max_salary}")
    

    return result

# geeting the employees above threshold age
def get_employees_above_threshold_age(age):
    age=int(age)
    logger.info(f"API REQUEST: Filtering of employees based on threshold age from total {len(employees)} employees")
    filtered_employees=[emp for emp in employees if emp.get_age()>age]
     
    result = [emp.to_dict() for emp in filtered_employees]
    logger.info(f"API RESPONSE: Returning {len(result)} employees above the threshold age= '{age},")
    return result

#getting the employees between age limits
def get_employees_between_age_limit(lower_age_limit,upper_age_limit):
    upper_age_limit=int(upper_age_limit)
    lower_age_limit=int(lower_age_limit)
    logger.info(f"API REQUEST: Flitering of employees between age limits from total {len(employees)} employees")
    filtered_employees=[emp for emp in employees if lower_age_limit<emp.get_age()<upper_age_limit]
    
    result = [emp.to_dict() for emp in filtered_employees]
    logger.info(f"API RESPONSE: Returning {len(result)} employees between age limits'{upper_age_limit}' and '{lower_age_limit}'")

    return result 

#get the employees under the project specified
def get_employees_undre_project(project_name):
    logger.info(f"API REQUEST: Flitering of employees under the specified project from total {len(employees)} employees")
    filtered_employees=[emp for emp in employees if any(project.name.lower()==project_name.lower() for project in emp.projects)]
        
    result = [emp.to_dict() for emp in filtered_employees]
    logger.info(f"API RESPONSE: Returning {len(result)} employees under the project  '{project_name}'")

    return result 

