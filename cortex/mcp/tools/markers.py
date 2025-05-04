"""
Ferramenta MCP para escaneamento de marcadores no código (TODOs, FIXMEs, etc).
"""

import os
import re
from glob import glob
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union

import structlog

# Configuração de logger
logger = structlog.get_logger()

# Tipos de marcadores suportados
MARKER_TYPES = {
    "TODO": re.compile(r"TODO\s*:?\s*(.*?)(?:\n|$)"),
    "FIXME": re.compile(r"FIXME\s*:?\s*(.*?)(?:\n|$)"),
    "HACK": re.compile(r"HACK\s*:?\s*(.*?)(?:\n|$)"),
    "BUG": re.compile(r"BUG\s*:?\s*(.*?)(?:\n|$)"),
    "NOTE": re.compile(r"NOTE\s*:?\s*(.*?)(?:\n|$)"),
    "REVIEW": re.compile(r"REVIEW\s*:?\s*(.*?)(?:\n|$)"),
}

# Extensões de arquivo suportadas por padrão
DEFAULT_EXTENSIONS = [
    ".py", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".scss", 
    ".c", ".cpp", ".h", ".hpp", ".java", ".go", ".rs", ".rb", ".php"
]

# Diretórios a serem ignorados por padrão
DEFAULT_IGNORE_DIRS = [
    "node_modules", "venv", ".venv", ".git", "__pycache__", 
    "dist", "build", "target", "out", ".idea", ".vscode"
]


def scan_markers(
    path: str = ".",
    include_pattern: Optional[str] = None,
    exclude_pattern: Optional[str] = None,
    marker_types: Optional[List[str]] = None,
    ignore_dirs: Optional[List[str]] = None,
    max_results: int = 100,
) -> Dict:
    """
    Escaneia arquivos em busca de marcadores como TODOs e FIXMEs.
    
    Args:
        path: Diretório para escanear
        include_pattern: Padrão glob para incluir arquivos (ex: "*.py,*.js")
        exclude_pattern: Padrão glob para excluir arquivos (ex: "test_*,*_test.py")
        marker_types: Tipos de marcador a procurar (ex: ["TODO", "FIXME"])
        ignore_dirs: Diretórios a ignorar
        max_results: Número máximo de resultados a retornar
        
    Returns:
        Dict: Marcadores encontrados agrupados por tipo e arquivo
    """
    try:
        logger.info(
            "Escaneando marcadores", 
            path=path, 
            include_pattern=include_pattern, 
            marker_types=marker_types
        )
        
        # Normalizar para Path
        base_path = Path(path).resolve()
        
        if not base_path.exists():
            return {
                "success": False,
                "error": "Diretório não encontrado",
                "message": f"O diretório '{path}' não existe"
            }
        
        # Definir tipos de marcador a procurar
        if marker_types:
            markers_to_find = {}
            for marker in marker_types:
                if marker.upper() in MARKER_TYPES:
                    markers_to_find[marker.upper()] = MARKER_TYPES[marker.upper()]
        else:
            markers_to_find = MARKER_TYPES
        
        # Definir padrões de inclusão/exclusão
        inclusion_patterns = []
        if include_pattern:
            for pattern in include_pattern.split(","):
                pattern = pattern.strip()
                if not pattern.startswith("*"):
                    pattern = f"**/{pattern}"
                inclusion_patterns.append(pattern)
        else:
            # Padrão: todos os arquivos com extensões suportadas
            for ext in DEFAULT_EXTENSIONS:
                inclusion_patterns.append(f"**/*{ext}")
        
        exclusion_patterns = []
        if exclude_pattern:
            for pattern in exclude_pattern.split(","):
                pattern = pattern.strip()
                if not pattern.startswith("*"):
                    pattern = f"**/{pattern}"
                exclusion_patterns.append(pattern)
        
        # Definir diretórios a ignorar
        dirs_to_ignore = set(DEFAULT_IGNORE_DIRS)
        if ignore_dirs:
            dirs_to_ignore.update(ignore_dirs)
        
        # Resultados
        results = []
        
        # Função para verificar se um caminho deve ser ignorado
        def should_ignore(file_path: Path) -> bool:
            parts = file_path.parts
            for ignore_dir in dirs_to_ignore:
                if ignore_dir in parts:
                    return True
            return False
        
        # Obter arquivos correspondentes aos padrões
        all_files = set()
        for pattern in inclusion_patterns:
            matched_files = set(base_path.glob(pattern))
            all_files.update(matched_files)
        
        # Remover arquivos excluídos
        for pattern in exclusion_patterns:
            excluded_files = set(base_path.glob(pattern))
            all_files.difference_update(excluded_files)
        
        # Filtrar diretórios ignorados
        all_files = {f for f in all_files if f.is_file() and not should_ignore(f)}
        
        # Escanear cada arquivo
        for file_path in all_files:
            try:
                relative_path = file_path.relative_to(base_path)
                
                # Ler conteúdo do arquivo
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                line_index = 1
                for line in content.splitlines():
                    # Verificar cada tipo de marcador
                    for marker_type, marker_regex in markers_to_find.items():
                        matches = marker_regex.findall(line)
                        for match in matches:
                            results.append({
                                "file": str(relative_path),
                                "line": line_index,
                                "type": marker_type,
                                "text": match.strip() if match.strip() else f"{marker_type} sem descrição",
                                "full_line": line.strip()
                            })
                            
                            # Limitar resultados
                            if len(results) >= max_results:
                                logger.warning(
                                    "Limite máximo de resultados atingido", 
                                    limit=max_results
                                )
                                break
                        
                        # Verificar limite novamente
                        if len(results) >= max_results:
                            break
                    
                    line_index += 1
                    
                    # Verificar limite novamente
                    if len(results) >= max_results:
                        break
            
            except UnicodeDecodeError:
                # Ignorar arquivos binários
                logger.debug("Ignorando arquivo binário", file=str(file_path))
                continue
            except Exception as e:
                logger.warning(
                    "Erro ao processar arquivo", 
                    file=str(file_path), 
                    error=str(e)
                )
                continue
            
            # Verificar limite novamente
            if len(results) >= max_results:
                break
        
        # Agrupar resultados por tipo de marcador
        results_by_type = {}
        for marker_type in markers_to_find.keys():
            results_by_type[marker_type] = [r for r in results if r["type"] == marker_type]
        
        # Agrupar resultados por arquivo
        results_by_file = {}
        for result in results:
            file_path = result["file"]
            if file_path not in results_by_file:
                results_by_file[file_path] = []
            results_by_file[file_path].append(result)
        
        logger.info(
            "Escaneamento concluído",
            total=len(results),
            files_scanned=len(all_files)
        )
        
        return {
            "success": True,
            "markers": results,
            "by_type": results_by_type,
            "by_file": results_by_file,
            "total": len(results),
            "files_scanned": len(all_files),
            "truncated": len(results) >= max_results
        }
    
    except Exception as e:
        logger.error("Erro ao escanear marcadores", error=str(e), path=path)
        return {
            "success": False,
            "error": str(e),
            "message": f"Falha ao escanear marcadores: {str(e)}"
        } 