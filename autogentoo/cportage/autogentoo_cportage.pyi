from typing import Optional, Dict


class AtomVersion:
    raw: str

    def __init__(self, version_string: str): ...
    def __cmp__(self, other: AtomVersion): ...


class UseFlag:
    name: str
    state: bool

    def __init__(self, name: str, state: bool): ...

class AtomFlag:
    name: str
    option: int
    default: int
    next: Optional['AtomFlag']

    def __init__(self, expr: str): ...
    def __next__(self) -> AtomFlag: ...
    def __iter__(self) -> AtomFlag: ...


class Package:
    package_id: int
    category: str
    name: str
    key: str
    ebuilds: Ebuild

    def __init__(self, key: str): ...
    def add_ebuild(self, ebuild: Ebuild): ...
    def match_atom(self, atom: Atom): ...

    def __iter__(self) -> Ebuild: ...


class Portage:
    def __init__(self): ...
    def add_package(self, package: Package): ...
    def get_package(self, package_id: int) -> 'Package': ...
    def match_atom(self, atom: Atom) -> Ebuild: ...
    def get_use_flag(self, use_flag: int) -> UseFlag: ...
    def initialize_repository(self, ebuild_path: Optional[str], cache_path: str) -> int: ...


class RequiredUse:
    name: str
    id: int
    operator: int
    depend: 'RequiredUse'
    next: 'RequiredUse'
    def __init__(self, required_use_string: str): ...
    def __next__(self) -> 'RequiredUse': ...
    def __iter__(self) -> 'RequiredUse': ...


class Atom:
    id: int
    category: str
    name: str

    key: str
    repository: str

    slot: str
    sub_slot: str
    slot_opts: int

    range: int
    blocks: int
    revision: int

    version: AtomVersion
    useflags: AtomFlag

    def __init__(self, atom_string: str): ...
    def matches(self, ebuild: Ebuild) -> bool: ...
    def __hash__(self) -> int: ...


class Dependency:
    use_operator: int
    use_condition: int
    atom: Atom

    def __init__(self, depend_string: str): ...

    children: Optional['Dependency']
    next: Optional['Dependency']

    def __next__(self) -> 'Dependency': ...
    def __iter__(self) -> 'Dependency': ...

class Ebuild:
    name: str
    category: str
    slot: str
    sub_slot: str
    package_key: str
    key: str
    ebuild: str
    path: str
    cache_file: str
    iuse: Dict[str, UseFlag]

    depend: Optional[Dependency]
    bdepend: Optional[Dependency]
    rdepend: Optional[Dependency]
    pdepend: Optional[Dependency]

    required_use: RequiredUse
    src_uri: Dependency

    version: AtomVersion
    metadata_init: bool

    package: Package
    older: Optional[Ebuild]
    newer: Optional[Ebuild]

    def __init__(self,
                 ebuild_repo: Optional[str],
                 cache_repo: str,
                 category: str,
                 name_and_version: str): ...

    def initialize_metadata(self): ...

    def __next__(self) -> "Ebuild": ...

def init(portage: Optional[Portage]): ...
def get_portage() -> Portage: ...

# /* use_operator_t */
USE_OP_DISABLE: int = ...
USE_OP_ENABLE: int = ...
USE_OP_LEAST_ONE: int = ...
USE_OP_EXACT_ONE: int = ...
USE_OP_MOST_ONE: int = ...

# /* use_state_t */
USE_STATE_UNKNOWN: int = ...
USE_STATE_DISABLED: int = ...
USE_STATE_ENABLED: int = ...

# /* atom_use_t */
ATOM_USE_DISABLE: int = ...
ATOM_USE_ENABLE: int = ...
ATOM_USE_ENABLE_IF_ON: int = ...
ATOM_USE_DISABLE_IF_OFF: int = ...
ATOM_USE_EQUAL: int = ...
ATOM_USE_OPPOSITE: int = ...

# /* atom_use_default_t */
ATOM_DEFAULT_NONE: int = ...
ATOM_DEFAULT_ON: int = ...
ATOM_DEFAULT_OFF: int = ...

# /* atom_version_t */
ATOM_VERSION_NONE: int = ...
ATOM_VERSION_E: int = ...
ATOM_VERSION_L: int = ...
ATOM_VERSION_G: int = ...
ATOM_VERSION_REV: int = ...
ATOM_VERSION_ALL: int = ...
ATOM_VERSION_GE: int = ...
ATOM_VERSION_LE: int = ...

# /* atom_block_t */
ATOM_BLOCK_NONE: int = ...
ATOM_BLOCK_SOFT: int = ...
ATOM_BLOCK_HARD: int = ...

# /* atom_slot_t */
ATOM_SLOT_IGNORE: int = ...
ATOM_SLOT_REBUILD: int = ...

# /* atom_version_pre_t */
ATOM_PREFIX_ALPHA: int = ...
ATOM_PREFIX_BETA: int = ...
ATOM_PREFIX_PRE: int = ...
ATOM_PREFIX_RC: int = ...
ATOM_PREFIX_NONE: int = ...
ATOM_PREFIX_P: int = ...

# /* arch_t */
ARCH_AMD64: int = ...
ARCH_X86: int = ...
ARCH_ARM: int = ...
ARCH_ARM64: int = ...
ARCH_HPPA: int = ...
ARCH_IA64: int = ...
ARCH_PPC: int = ...
ARCH_PPC64: int = ...
ARCH_SPARC: int = ...
ARCH_END: int = ...

# /* keyword_t */
KEYWORD_BROKEN: int = ...
KEYWORD_NONE: int = ...
KEYWORD_UNSTABLE: int = ...
KEYWORD_STABLE: int = ...
