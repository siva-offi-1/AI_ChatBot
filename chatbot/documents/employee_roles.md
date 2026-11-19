# Employee Roles and Access

Company: Northstar Holdings
Document Status: Canonical
Last Updated: 2026-09-01

## Purpose
This document defines the main user roles used in the Northstar Holdings ERP.

## Employee
Employees may view their own profile and attendance, apply for leave, submit attendance correction requests, view their own payslips, and submit flight ticket requests when eligible.
Employees must not access another employee's private HR records.

## Direct Manager
A Direct Manager has authority only over employees assigned to them.
They may review leave requests and missing punch requests for assigned employees and view their attendance.
They do not automatically have access to employee salary, payslips, bank information, or private HR documents.

## HR
HR users may review HR workflow requests, manage employee information when authorized, review attendance requests, and process leave requests.
HR access to payroll information requires separate payroll authorization.

## HR Admin
HR Admin users may configure HR policies, manage workflow settings, cancel fully approved leave when company policy permits, and manage role and manager assignments.
Important HR Admin actions must be audited.

## Payroll HR
Payroll HR may view payroll records, review payslips, and resolve payroll-related employee support requests.
Payroll HR access does not automatically grant HR Admin configuration authority.

## Security Principle
A role supplied by the browser, request body, chatbot prompt, or frontend must not be trusted as proof of authorization.
Authorization must be verified by the backend application.
