# Arsitektur Aplikasi dan Struktur Folder — educoffee POS

## A. Diagram Arsitektur Berlapis (MVC)
```mermaid
flowchart LR
  U([Pengguna: Peramban]) -->|HTTP request| R
  subgraph APP["Aplikasi Flask"]
    R["Routes / Controller (app.py)"] --> S["Logika Bisnis (services.py)"]
    S --> M["Model / Akses Data (models.py)"]
    R --> V["View: templates/*.html"]
  end
  M -->|SQL Queries| DB[(SQLite: kopikita.db)]
  V -->|HTML Response| U