#!/usr/bin/env python3
"""
Validate API route path follows REST conventions.

Ensures routes are RESTful, properly formatted, and follow best practices.
"""

import sys
import re
import argparse

# HTTP methods and their typical use cases
HTTP_METHODS = {
    'GET': 'Retrieve resource(s)',
    'POST': 'Create new resource',
    'PUT': 'Replace entire resource',
    'PATCH': 'Update part of resource',
    'DELETE': 'Remove resource',
}

def validate_route_path(path, method=None):
    """
    Validate route path against REST conventions.

    Args:
        path: API route path
        method: HTTP method (optional)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check path starts with /
    if not path.startswith('/'):
        return False, "Route path must start with '/'"

    # Check no trailing slash (except for root)
    if len(path) > 1 and path.endswith('/'):
        return False, "Route path should not end with '/' (except root '/')"

    # Check for double slashes
    if '//' in path:
        return False, "Route path contains double slashes '//'"

    # Check path segments
    segments = [s for s in path.split('/') if s]

    # Check resource naming (should be plural for collections)
    for i, segment in enumerate(segments):
        # Skip API prefix and version
        if segment in ('api', 'v1', 'v2', 'v3'):
            continue

        # Skip path parameters
        if segment.startswith(':') or (segment.startswith('{') and segment.endswith('}')):
            continue

        # Check resource naming
        if not segment.islower():
            return False, f"Resource '{segment}' should be lowercase"

        # Check for underscores vs hyphens (prefer hyphens)
        if '_' in segment:
            suggested = segment.replace('_', '-')
            return False, f"Use hyphens instead of underscores: '{segment}' → '{suggested}'"

    # Method-specific validation
    if method:
        method = method.upper()
        if method not in HTTP_METHODS:
            return False, f"Invalid HTTP method: {method}. Use: {', '.join(HTTP_METHODS.keys())}"

        # Check method matches path intent
        if method == 'POST' and segments and segments[-1].startswith(':'):
            return False, "POST endpoints should target collections, not specific resources (remove :id)"

        if method in ('PUT', 'PATCH', 'DELETE'):
            # These methods typically need an ID parameter
            if not any(s.startswith(':') or (s.startswith('{') and s.endswith('}')) for s in segments):
                return False, f"{method} endpoints typically need a resource ID parameter (e.g., /:id)"

    return True, None

def suggest_valid_path(path):
    """
    Suggest a valid route path if the provided one is invalid.

    Args:
        path: Invalid route path

    Returns:
        str: Suggested valid path
    """
    # Remove trailing slash
    if path.endswith('/') and len(path) > 1:
        path = path.rstrip('/')

    # Fix double slashes
    while '//' in path:
        path = path.replace('//', '/')

    # Convert to lowercase and replace underscores
    segments = path.split('/')
    fixed_segments = []
    for segment in segments:
        if segment.startswith(':') or (segment.startswith('{') and segment.endswith('}')):
            fixed_segments.append(segment)
        else:
            fixed_segments.append(segment.lower().replace('_', '-'))

    suggested = '/'.join(fixed_segments)

    # Ensure starts with /
    if not suggested.startswith('/'):
        suggested = '/' + suggested

    return suggested

def main():
    parser = argparse.ArgumentParser(description='Validate REST API route path')
    parser.add_argument('--path', required=True, help='Route path to validate')
    parser.add_argument('--method', help='HTTP method (GET, POST, PUT, PATCH, DELETE)')
    parser.add_argument('--suggest', action='store_true', help='Suggest a valid path if invalid')

    args = parser.parse_args()

    is_valid, error = validate_route_path(args.path, args.method)

    if is_valid:
        print(f"✅ '{args.path}' is a valid route path")
        if args.method:
            print(f"   Method: {args.method.upper()} - {HTTP_METHODS[args.method.upper()]}")
        sys.exit(0)
    else:
        print(f"❌ Invalid route path: {error}", file=sys.stderr)

        if args.suggest:
            suggested = suggest_valid_path(args.path)
            print(f"💡 Suggested path: {suggested}", file=sys.stderr)

        sys.exit(1)

if __name__ == '__main__':
    main()
