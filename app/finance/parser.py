import pandas as pd
import json
from datetime import datetime
from typing import List, Dict, Any
import re

class RBCParser:
    """Parse RBC bank statements in CSV format"""
    
    @staticmethod
    def detect_format(df):
        """Detect the format of the uploaded CSV"""
        columns = df.columns.tolist()
        
        # Format B: RBC CSV export
        if 'CAD$' in columns and 'Transaction Date' in columns:
            return 'rbc_csv'
        
        # Format A: PDF table extract
        elif 'Withdrawals ($)' in columns and 'Deposits ($)' in columns:
            return 'rbc_pdf_table'
        
        else:
            raise ValueError("Unsupported CSV format")
    
    @staticmethod
    def parse_rbc_csv(df: pd.DataFrame) -> List[Dict]:
        """Parse Format B: RBC CSV export"""
        transactions = []
        
        for _, row in df.iterrows():
            # Get amount from CAD$ column
            amount_str = str(row['CAD$']).replace(',', '')
            if not amount_str or amount_str == 'nan':
                continue
                
            amount = float(amount_str)
            
            # Determine type based on amount sign
            if amount > 0:
                trans_type = 'income'
            elif amount < 0:
                trans_type = 'expense'
                amount = abs(amount)  # Store positive for expenses
            else:
                continue
            
            # Combine descriptions
            desc1 = str(row['Description 1']) if pd.notna(row['Description 1']) else ''
            desc2 = str(row['Description 2']) if pd.notna(row['Description 2']) else ''
            description = f"{desc1} {desc2}".strip()
            
            # Parse date (handle multiple formats)
            date_str = str(row['Transaction Date'])
            transaction_date = RBCParser.parse_date(date_str)
            
            transactions.append({
                'transaction_date': transaction_date,
                'description': description,
                'amount': amount,
                'type': trans_type,
                'raw_data': row.to_dict()
            })
        
        return transactions
    
    @staticmethod
    def parse_rbc_pdf_table(df: pd.DataFrame) -> List[Dict]:
        """Parse Format A: PDF table extract"""
        transactions = []
        
        for _, row in df.iterrows():
            # Skip empty rows
            if pd.isna(row.get('Date')) or pd.isna(row.get('Description')):
                continue
            
            # Determine amount from withdrawals or deposits
            withdrawal = row.get('Withdrawals ($)')
            deposit = row.get('Deposits ($)')
            
            amount = 0
            trans_type = ''
            
            if pd.notna(withdrawal) and str(withdrawal).strip():
                amount = float(str(withdrawal).replace(',', '').replace('$', '').strip())
                trans_type = 'expense'
            elif pd.notna(deposit) and str(deposit).strip():
                amount = float(str(deposit).replace(',', '').replace('$', '').strip())
                trans_type = 'income'
            else:
                continue
            
            # Parse date
            date_str = str(row['Date'])
            transaction_date = RBCParser.parse_date(date_str)
            
            transactions.append({
                'transaction_date': transaction_date,
                'description': str(row['Description']).strip(),
                'amount': amount,
                'type': trans_type,
                'raw_data': row.to_dict()
            })
        
        return transactions
    
    @staticmethod
    def parse_date(date_str: str) -> str:
        """Parse various date formats"""
        date_str = str(date_str).strip()
        
        # Remove any time portion
        date_str = date_str.split()[0]
        
        # Try different formats
        formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%d-%m-%Y',
            '%m-%d-%Y',
            '%d.%m.%Y',
            '%Y/%m/%d'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        # If all fail, return as-is
        return date_str
