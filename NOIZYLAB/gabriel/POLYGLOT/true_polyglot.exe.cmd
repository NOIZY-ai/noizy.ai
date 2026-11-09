#!/bin/bash
#|| @goto batch
: << 'BASH_ONLY'
BASH_ONLY
# Shell/Bash execution path
echo "Bash/Zsh/Shell"
exit 0

:batch
@echo off
echo Windows Batch
exit /b 0

: << 'POLYGLOT_DOCS'
=pod

=head1 NAME

true_polyglot - Runs natively in Bash AND Windows Batch

=head1 USAGE

  # Unix/Mac
  bash true_polyglot.exe.cmd
  
  # Windows  
  true_polyglot.exe.cmd

=cut
POLYGLOT_DOCS
