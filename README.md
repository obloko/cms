# cms

This project is meant to be a foundation for working with data. Project uses Django as framework.

Main tenants are:

1. Database abstraction
 * Relational (PostgreSQL, MySQL, Oracle and SQLite) and document (MongoDB) databases support
 * Machine-usable schema abstraction
 * Database-specific type and constrain support
 * Code generation from database-specific model
 * Schema versioning
2. Data Modeling and Management Tools
 * Schema visualization and management model abstraction
 * Visual schema model management 
 * Table-driven schema visualization and management
 * Customizable per-type schema visualization and management 
 * Code generation from visual model abstraction
3. API generation
 * Automatic API generation based on models
 * API model abstraction
 * Code generation from API model abstraction
4. Content and Code Management
 * Content curation workflow configuration
 * Publishing, Versioning, Version Tagging
5. Import and Ingest
 * Import job configuration
 * Import data mapping tools
 * Intergrations, Webhooks and callbacks
 * Workflow tools
6. Reports
 * Reporting abstraction model
 * Dashboards
 * Spark integration
