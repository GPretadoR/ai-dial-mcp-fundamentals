from pathlib import Path
import json

from mcp.server.fastmcp import FastMCP

from models.user_info import UserSearchRequest, UserCreate, UserUpdate
from user_client import UserClient

# Create instance of FastMCP
mcp = FastMCP(
    name="users-management-mcp-server",
    host="0.0.0.0",
    port=8005,
)

# Create UserClient
user_client = UserClient()


# ==================== TOOLS ====================

@mcp.tool()
async def get_user_by_id(user_id: int) -> str:
    """Retrieves a user by their ID from the User Management Service.
    
    Use this tool when you need to get detailed information about a specific user.
    
    Args:
        user_id: The unique identifier of the user to retrieve
        
    Returns:
        A formatted string containing the user's complete profile information including
        personal details, contact information, address, and other attributes.
        Returns an error message if the user is not found.
    """
    try:
        result = await user_client.get_user(user_id)
        return result
    except Exception as e:
        return f"Error getting user: {str(e)}"


@mcp.tool()
async def search_user(
    name: str | None = None,
    surname: str | None = None,
    email: str | None = None,
    gender: str | None = None
) -> str:
    """Search for users in the User Management Service by various criteria.
    
    Use this tool to find users based on name, surname, email, or gender.
    All search parameters support partial matching (case-insensitive).
    You can combine multiple criteria to narrow down results.
    
    Args:
        name: First name to search for (partial matching supported)
        surname: Last name to search for (partial matching supported)
        email: Email address to search for (partial matching supported)
        gender: Gender to filter by (exact match: male, female, other, prefer_not_to_say)
        
    Returns:
        A formatted string containing all matching users with their details.
        Returns the count of users found and their complete information.
    """
    try:
        result = await user_client.search_users(
            name=name,
            surname=surname,
            email=email,
            gender=gender
        )
        return result
    except Exception as e:
        return f"Error searching users: {str(e)}"


@mcp.tool()
async def add_user(user: UserCreate) -> str:
    """Create a new user in the User Management Service.
    
    Use this tool to add a new user profile to the system.
    Required fields: name, surname, email, about_me.
    Optional fields: phone, date_of_birth, gender, company, salary, address, credit_card.
    
    Args:
        user: A UserCreate object containing all the user information.
              Required fields: name, surname, email, about_me
              
    Returns:
        A success message with the created user's information,
        or an error message if the creation failed.
    """
    try:
        result = await user_client.add_user(user)
        return result
    except Exception as e:
        return f"Error adding user: {str(e)}"


@mcp.tool()
async def update_user(user_id: int, user: UserUpdate) -> str:
    """Update an existing user's information in the User Management Service.
    
    Use this tool to modify an existing user's profile.
    All fields are optional - only provide the fields you want to update.
    
    Args:
        user_id: The unique identifier of the user to update
        user: A UserUpdate object containing the fields to update.
              All fields are optional.
              
    Returns:
        A success message confirming the update,
        or an error message if the update failed.
    """
    try:
        result = await user_client.update_user(user_id, user)
        return result
    except Exception as e:
        return f"Error updating user: {str(e)}"


@mcp.tool()
async def delete_user(user_id: int) -> str:
    """Delete a user from the User Management Service.
    
    Use this tool to permanently remove a user from the system.
    This operation cannot be undone.
    
    Args:
        user_id: The unique identifier of the user to delete
        
    Returns:
        A success message confirming the deletion,
        or an error message if the deletion failed.
    """
    try:
        result = await user_client.delete_user(user_id)
        return result
    except Exception as e:
        return f"Error deleting user: {str(e)}"


# ==================== MCP RESOURCES ====================

@mcp.resource(uri="users-management://flow-diagram", mime_type="image/png")
async def get_flow_diagram() -> bytes:
    """Provides the architecture flow diagram showing how the MCP server integrates with the User Management Service.
    
    This resource contains a visual representation of the data flow between
    the Agent, MCP Server, and User Management Service.
    """
    diagram_path = Path(__file__).parent / "flow.png"
    return diagram_path.read_bytes()


# ==================== MCP PROMPTS ====================

@mcp.prompt()
async def search_strategy_prompt() -> str:
    """Provides guidance on formulating effective user search queries.
    
    This prompt helps users understand how to use the search functionality effectively,
    including available parameters, search strategies, and example patterns.
    """
    return """You are helping users search through a dynamic user database. The database contains 
realistic synthetic user profiles with the following searchable fields:

## Available Search Parameters
- **name**: First name (partial matching, case-insensitive)
- **surname**: Last name (partial matching, case-insensitive)  
- **email**: Email address (partial matching, case-insensitive)
- **gender**: Exact match (male, female, other, prefer_not_to_say)

## Search Strategy Guidance

### For Name Searches
- Use partial names: "john" finds John, Johnny, Johnson, etc.
- Try common variations: "mike" vs "michael", "liz" vs "elizabeth"
- Consider cultural name variations

### For Email Searches  
- Search by domain: "gmail" for all Gmail users
- Search by name patterns: "john" for emails containing john
- Use company names to find business emails

### For Demographic Analysis
- Combine gender with other criteria for targeted searches
- Use broad searches first, then narrow down

### Effective Search Combinations
- Name + Gender: Find specific demographic segments
- Email domain + Surname: Find business contacts
- Partial names: Cast wider nets for common names

## Example Search Patterns
```
"Find all Johns" → name="john"
"Gmail users named Smith" → email="gmail" + surname="smith"  
"Female users with company emails" → gender="female" + email="company"
"Users with Johnson surname" → surname="johnson"
```

## Tips for Better Results
1. Start broad, then narrow down
2. Try variations of names (John vs Johnny)
3. Use partial matches creatively
4. Combine multiple criteria for precision
5. Remember searches are case-insensitive

When helping users search, suggest multiple search strategies and explain 
why certain approaches might be more effective for their goals."""


@mcp.prompt()
async def user_creation_prompt() -> str:
    """Provides comprehensive guidelines for creating realistic and valid user profiles.
    
    This prompt includes field requirements, validation rules, and best practices
    for creating user profiles with appropriate and realistic data.
    """
    return """You are helping create realistic user profiles for the system. Follow these guidelines 
to ensure data consistency and realism.

## Required Fields
- **name**: 2-50 characters, letters only, culturally appropriate
- **surname**: 2-50 characters, letters only  
- **email**: Valid format, must be unique in system
- **about_me**: Rich, realistic biography (see guidelines below)

## Optional Fields Best Practices
- **phone**: Use E.164 format (+1234567890) when possible
- **date_of_birth**: YYYY-MM-DD format, realistic ages (18-80)
- **gender**: Use standard values (male, female, other, prefer_not_to_say)
- **company**: Real-sounding company names
- **salary**: $30,000-$200,000 range for employed individuals

## Address Guidelines
Provide complete, realistic addresses:
- **country**: Full country names
- **city**: Actual city names  
- **street**: Realistic street addresses
- **flat_house**: Apartment/unit format (Apt 123, Unit 5B, Suite 200)

## Credit Card Guidelines  
Generate realistic but non-functional card data:
- **num**: 16 digits formatted as XXXX-XXXX-XXXX-XXXX
- **cvv**: 3 digits (000-999)
- **exp_date**: MM/YYYY format, future dates only

## Biography Creation ("about_me")
Create engaging, realistic biographies that include:

### Personality Elements
- 1-3 personality traits (curious, adventurous, analytical, etc.)
- Authentic voice and writing style
- Cultural and demographic appropriateness

### Interests & Hobbies  
- 2-4 specific hobbies or activities
- 1-3 broader interests or passion areas
- 1-2 life goals or aspirations

### Biography Templates
Use varied narrative structures:
- "I'm a [trait] person who loves [hobbies]..."
- "When I'm not working, you can find me [activity]..."  
- "Life is all about balance for me. I enjoy [interests]..."
- "As someone who's [trait], I find great joy in [hobby]..."

## Data Validation Reminders
- Email uniqueness is enforced (check existing users)
- Phone numbers should follow consistent formatting
- Date formats must be exact (YYYY-MM-DD)
- Credit card expiration dates must be in the future
- Salary values should be realistic for the demographic

## Cultural Sensitivity
- Match names to appropriate cultural backgrounds
- Consider regional variations in address formats
- Use realistic company names for the user's location
- Ensure hobbies and interests are culturally appropriate

When creating profiles, aim for diversity in:
- Geographic representation
- Age distribution  
- Interest variety
- Socioeconomic backgrounds
- Cultural backgrounds"""
"""


# Guides creation of realistic user profiles
"""
You are helping create realistic user profiles for the system. Follow these guidelines 
to ensure data consistency and realism.

## Required Fields
- **name**: 2-50 characters, letters only, culturally appropriate
- **surname**: 2-50 characters, letters only  
- **email**: Valid format, must be unique in system
- **about_me**: Rich, realistic biography (see guidelines below)

## Optional Fields Best Practices
- **phone**: Use E.164 format (+1234567890) when possible
- **date_of_birth**: YYYY-MM-DD format, realistic ages (18-80)
- **gender**: Use standard values (male, female, other, prefer_not_to_say)
- **company**: Real-sounding company names
- **salary**: $30,000-$200,000 range for employed individuals

## Address Guidelines
Provide complete, realistic addresses:
- **country**: Full country names
- **city**: Actual city names  
- **street**: Realistic street addresses
- **flat_house**: Apartment/unit format (Apt 123, Unit 5B, Suite 200)

## Credit Card Guidelines  
Generate realistic but non-functional card data:
- **num**: 16 digits formatted as XXXX-XXXX-XXXX-XXXX
- **cvv**: 3 digits (000-999)
- **exp_date**: MM/YYYY format, future dates only

## Biography Creation ("about_me")
Create engaging, realistic biographies that include:

### Personality Elements
- 1-3 personality traits (curious, adventurous, analytical, etc.)
- Authentic voice and writing style
- Cultural and demographic appropriateness

### Interests & Hobbies  
- 2-4 specific hobbies or activities
- 1-3 broader interests or passion areas
- 1-2 life goals or aspirations

### Biography Templates
Use varied narrative structures:
- "I'm a [trait] person who loves [hobbies]..."
- "When I'm not working, you can find me [activity]..."  
- "Life is all about balance for me. I enjoy [interests]..."
- "As someone who's [trait], I find great joy in [hobby]..."

## Data Validation Reminders
- Email uniqueness is enforced (check existing users)
- Phone numbers should follow consistent formatting
- Date formats must be exact (YYYY-MM-DD)
- Credit card expiration dates must be in the future
- Salary values should be realistic for the demographic

## Cultural Sensitivity
- Match names to appropriate cultural backgrounds
- Consider regional variations in address formats
- Use realistic company names for the user's location
- Ensure hobbies and interests are culturally appropriate

When creating profiles, aim for diversity in:
- Geographic representation
- Age distribution  
- Interest variety
- Socioeconomic backgrounds
- Cultural backgrounds"""


if __name__ == "__main__":
    # Run server with streamable-http transport
    mcp.run(transport="streamable-http")
