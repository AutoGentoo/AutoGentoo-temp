cdef class DynamicBuffer:
	cdef void* ptr
	cdef size_t size
	cdef public size_t n
	cdef short align
	
	cdef realloc (self)
	cdef void append (self, void* ptr, size_t size)
	cdef void append_string (self, char* ptr)
	cdef void set (self, void* ptr, int start, size_t size)
	cpdef void print_raw (self, align=*)

cdef class Binary(DynamicBuffer):
	cdef size_t pos
	
	cdef char* read_string (self)
	cdef int read_int (self)
	cdef skip_until (self, to_find)
	cdef inside (self)
	cpdef read_template (self, char* template)