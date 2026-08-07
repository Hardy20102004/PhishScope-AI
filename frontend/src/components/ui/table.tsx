import React from "react";

export const Table: React.FC<React.HTMLAttributes<HTMLTableElement>> = ({ children, className = "", ...props }) => (
  <div className="w-full overflow-auto">
    <table className={`w-full caption-bottom text-sm ${className}`} {...props}>{children}</table>
  </div>
);

export const TableHeader: React.FC<React.HTMLAttributes<HTMLTableSectionElement>> = ({ children, className = "", ...props }) => (
  <thead className={`[&_tr]:border-b ${className}`} {...props}>{children}</thead>
);

export const TableBody: React.FC<React.HTMLAttributes<HTMLTableSectionElement>> = ({ children, className = "", ...props }) => (
  <tbody className={`[&_tr:last-child]:border-0 ${className}`} {...props}>{children}</tbody>
);

export const TableRow: React.FC<React.HTMLAttributes<HTMLTableRowElement>> = ({ children, className = "", ...props }) => (
  <tr className={`border-b transition-colors hover:bg-muted/50 ${className}`} {...props}>{children}</tr>
);

export const TableHead: React.FC<React.ThHTMLAttributes<HTMLTableCellElement>> = ({ children, className = "", ...props }) => (
  <th className={`h-12 px-4 text-left align-middle font-medium text-muted-foreground ${className}`} {...props}>{children}</th>
);

export const TableCell: React.FC<React.TdHTMLAttributes<HTMLTableCellElement>> = ({ children, className = "", ...props }) => (
  <td className={`p-4 align-middle ${className}`} {...props}>{children}</td>
);

export const TableFooter: React.FC<React.HTMLAttributes<HTMLTableSectionElement>> = ({ children, className = "", ...props }) => (
  <tfoot className={`border-t bg-muted/50 font-medium ${className}`} {...props}>{children}</tfoot>
);

export const TableCaption: React.FC<React.HTMLAttributes<HTMLTableCaptionElement>> = ({ children, className = "", ...props }) => (
  <caption className={`mt-4 text-sm text-muted-foreground ${className}`} {...props}>{children}</caption>
);
