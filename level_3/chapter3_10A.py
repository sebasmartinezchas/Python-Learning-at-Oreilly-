"""
Use Python's logging module. / Introducing Structured Logging
-- Key Topics --
- Logging vs Print Statements. Why logging is superior for production code.
- Log Levels: 
        - DEBUG: Detailed information, typically of interest only when diagnosing problems.
        - INFO: Confirmation that things are working as expected.
        - WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g., ‘disk space low’). The software is still working as expected.
        - ERROR: Due to a more serious problem, the software has not been able to perform some function.
        - CRITICAL: A serious error, indicating that the program itself may be unable to continue running.
- Structured Logging: Consistent, machine-readable log formats ( like JSON)
- Production Needs: Handlers for different destination (console,file)

-- Key Terms --
- Logger: The entry point to the logging system
- Handler: Send log records to a destinatiom
- Formatter: Specifies the layout and format of the log message.
- Log Level: A filter to control which messages get recorded.
- Structured  Logging: Logging in a predictable format to analysis.



"""