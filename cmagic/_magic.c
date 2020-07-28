#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include <magic.h>


typedef struct {
	PyObject_HEAD
	magic_t cookie;
} Magic;


static void Magic_dealloc(Magic *self) {
    if (self->cookie != NULL) magic_close(self->cookie);
}

static PyObject *
Magic_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
	Magic *self;

	self = (Magic *) type->tp_alloc(type, 0);
	return (PyObject *) self;
}

static int parse_flags(int *flags, PyObject* args, PyObject* kwds) {
    static char *kwlist[] = {
        "debug",
        "symlink",
        "compress",
        "devices",
        "mime_type",
        "mime_encoding",
        "all",
        "check",
        "preserve_atime",
        "raw",
        "error",
        "no_check_apptype",
        "no_check_ascii",
        "no_check_compress",
        "no_check_elf",
        "no_check_fortran",
        "no_check_soft",
        "no_check_tar",
        "no_check_tokens",
        "no_check_troff",
        NULL
    };

    int flag_debug = 0, flag_symlink = 0, flag_compress = 0, flag_devices = 0,
        flag_mime_type = 0, flag_mime_encoding = 0, flag_all = 0,
        flag_check = 0, flag_preserve_atime = 0, flag_raw = 0, flag_error = 0,
        flag_no_check_apptype = 0, flag_no_check_ascii = 0, flag_no_check_compress = 0,
        flag_no_check_elf = 0, flag_no_check_fortran = 0, flag_no_check_soft = 0,
        flag_no_check_tar = 0, flag_no_check_tokens = 0, flag_no_check_troff = 0;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "|pppppppppppppppppppp",
        kwlist,
        &flag_debug,
        &flag_symlink,
        &flag_compress,
        &flag_devices,
        &flag_mime_type,
        &flag_mime_encoding,
        &flag_all,
        &flag_check,
        &flag_preserve_atime,
        &flag_raw,
        &flag_error,
        &flag_no_check_apptype,
        &flag_no_check_ascii,
        &flag_no_check_compress,
        &flag_no_check_elf,
        &flag_no_check_fortran,
        &flag_no_check_soft,
        &flag_no_check_tar,
        &flag_no_check_tokens,
        &flag_no_check_troff
    )) return -1;

    if (flag_debug) flags[0] |= MAGIC_DEBUG;
    if (flag_symlink) flags[0] |= MAGIC_SYMLINK;
    if (flag_compress) flags[0] |= MAGIC_COMPRESS;
    if (flag_devices) flags[0] |= MAGIC_DEVICES;
    if (flag_mime_type) flags[0] |= MAGIC_MIME_TYPE;
    if (flag_mime_encoding) flags[0] |= MAGIC_MIME_ENCODING;
    if (flag_all) flags[0] |= MAGIC_CONTINUE;
    if (flag_check) flags[0] |= MAGIC_CHECK;
    if (flag_preserve_atime)  flags[0] |= MAGIC_PRESERVE_ATIME;
    if (flag_raw) flags[0] |= MAGIC_RAW;
    if (flag_error) flags[0] |= MAGIC_ERROR;
    if (flag_no_check_apptype) flags[0] |= MAGIC_NO_CHECK_APPTYPE;
    if (flag_no_check_ascii) flags[0] |= MAGIC_NO_CHECK_ASCII;
    if (flag_no_check_compress) flags[0] |= MAGIC_NO_CHECK_COMPRESS;
    if (flag_no_check_elf) flags[0] |= MAGIC_NO_CHECK_ELF;
    if (flag_no_check_fortran) flags[0] |= MAGIC_NO_CHECK_FORTRAN;
    if (flag_no_check_soft) flags[0] |= MAGIC_NO_CHECK_SOFT;
    if (flag_no_check_tar) flags[0] |= MAGIC_NO_CHECK_TAR;
    if (flag_no_check_tokens) flags[0] |= MAGIC_NO_CHECK_TOKENS;
    if (flag_no_check_troff) flags[0] |= MAGIC_NO_CHECK_TROFF;

    return 0;
}

static int Magic_init(Magic *self, PyObject *args, PyObject *kwds) {
	int flags = MAGIC_NONE;

	if (parse_flags(&flags, args, kwds)) return -1;

    self->cookie = magic_open(flags);

    if (self->cookie == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Can not allocate magic cookie");
        return -1;
    }

	return 0;
}

static PyObject* Magic_set_flags(Magic *self, PyObject* args,  PyObject *kwds) {

    int flags = MAGIC_NONE;
    if (parse_flags(&flags, args, kwds)) return NULL;

    if (magic_setflags(self->cookie, flags)) {
        PyErr_SetString(PyExc_RuntimeError, magic_error(self->cookie));
        return NULL;
    }

    Py_RETURN_NONE;
}

static PyObject* Magic_load(Magic *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = { "db_path", NULL };
    char *db_path;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "|s", kwlist, &db_path
    )) return NULL;

    if (db_path == NULL) db_path = getenv("MAGIC");

    int result;

    Py_BEGIN_ALLOW_THREADS;
    result = magic_load(self->cookie, db_path);
    Py_END_ALLOW_THREADS;

    if (result) {
        PyErr_SetString(PyExc_RuntimeError, magic_error(self->cookie));
        return NULL;
    }

    Py_RETURN_NONE;
}


static PyObject* Magic_check(Magic *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = { "db_path", NULL };
    char *db_path = NULL;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "|s", kwlist, &db_path
    )) return NULL;

    int result;

    if (db_path == NULL) db_path = getenv("MAGIC");

    Py_BEGIN_ALLOW_THREADS;
    result = magic_check(self->cookie, db_path);
    Py_END_ALLOW_THREADS;

    if (result) Py_RETURN_FALSE;
    Py_RETURN_TRUE;
}


static PyObject* Magic_compile(Magic *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = { "db_path", NULL };
    char *db_path;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "|s", kwlist, &db_path
    )) return NULL;

    if (db_path == NULL) db_path = getenv("MAGIC");

    int result;

    Py_BEGIN_ALLOW_THREADS;
    result = magic_compile(self->cookie, db_path);
    Py_END_ALLOW_THREADS;

    if (result) Py_RETURN_FALSE;
    Py_RETURN_TRUE;
}

static PyObject* Magic_file(Magic *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = { "filename", NULL };
    char *filename;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "s", kwlist, &filename
    )) return NULL;

    char * result;

    Py_BEGIN_ALLOW_THREADS;
    result = magic_file(self->cookie, filename);
    Py_END_ALLOW_THREADS;

    if (result == NULL) {
        PyErr_SetString(PyExc_RuntimeError, magic_error(self->cookie));
        return NULL;
    }

    return PyUnicode_FromString(result);
}


static PyObject* Magic_buffer(Magic *self, PyObject *args, PyObject *kwds) {
    static char *kwlist[] = { "payload", NULL };
    char *payload;
    Py_ssize_t length;

    if (!PyArg_ParseTupleAndKeywords(
        args, kwds, "y#", kwlist, &payload, &length
    )) return NULL;

    char * result;
    Py_BEGIN_ALLOW_THREADS;
    result = magic_buffer(self->cookie, payload, length);
    Py_END_ALLOW_THREADS;

    if (result == NULL) {
        PyErr_SetString(PyExc_RuntimeError, magic_error(self->cookie));
        return NULL;
    }

    return PyUnicode_FromString(result);
}


static PyObject* Magic_repr(Magic *self) {
	return PyUnicode_FromFormat(
        "<%s as %p>",
        Py_TYPE(self)->tp_name,  self
    );
}


static PyMemberDef Magic_members[] = {
	{NULL}  /* Sentinel */
};


static PyMethodDef Magic_methods[] = {
	{
		"load",
		(PyCFunction) Magic_load, METH_VARARGS | METH_KEYWORDS,
		(
		    "Must be used to load the the colon separated list\n"
		    "of database files passed in as filename, or None for the\n"
		    "default database file before any magic queries can performed."
		)
	},
	{
        "check",
        (PyCFunction) Magic_check, METH_VARARGS | METH_KEYWORDS,
        (
            "Can be used to check the validity of entries in the\n"
            "colon separated database files passed in as filename, or None\n"
            "for the default database. It returns True on success and False on failure."
        )
    },
    {
        "compile",
        (PyCFunction) Magic_compile, METH_VARARGS | METH_KEYWORDS,
        (
            "function can be used to compile the the colon separated list \n"
            "of database files passed in as filename, or NULL for the default \n"
            "database. It returns 0 on success and -1 on failure. The compiled \n"
            "files created are named from the basename(1) of each file argument \n"
            "with ''.mgc'' appended to it."
        )
    },
    {
        "guess_bytes",
        (PyCFunction) Magic_buffer, METH_VARARGS | METH_KEYWORDS,
        "Returns a textual description of the contents of the bytes argument"
    },
    {
        "guess_file",
        (PyCFunction) Magic_file, METH_VARARGS | METH_KEYWORDS,
        "Returns a textual description of the contents of the filename argument"
    },
    {
        "set_flags",
        (PyCFunction) Magic_set_flags, METH_VARARGS | METH_KEYWORDS,
        (
            "Set flags to Magic instance\n\n"
            ":param debug: Print debugging messages to stderr.\n"
            ":param symlink: If the file queried is a symlink, follow it.\n"
            ":param compress: If the file is compressed, unpack it and look at the contents.\n"
            ":param devices: If the file is a block or character special \n"
            "                device, then open the device and try to look in its contents.\n"
            ":param mime_type: Return a MIME type string, instead of a textual description.\n"
            ":param mime_encoding: Return a MIME encoding, instead of a textual description.\n"
            ":param all: Return all matches, not just the first.\n"
            ":param check: Check the magic database for consistency and print warnings to stderr.\n"
            ":param preserve_atime: On systems that support utime or utimes, attempt to \n"
            "                       preserve the access time of files analyzed.\n"
            ":param raw: Don't translate unprintable characters to a \\ooo octal representation.\n"
            ":param error: Treat operating system errors while trying to open files and \n"
            "              follow symlinks as real errors, instead of printing them \n"
            "              in the magic buffer.\n"
            ":param no_check_apptype: Check for EMX application type (only on EMX).\n"
            ":param no_check_ascii: Check for various types of ascii files.\n"
            ":param no_check_compress: Don't look for, or inside compressed files.\n"
            ":param no_check_elf: Don't print elf details.\n"
            ":param no_check_fortran: Don't look for fortran sequences inside ascii files.\n"
            ":param no_check_soft: Don't consult magic files.\n"
            ":param no_check_tar: Don't examine tar files.\n"
            ":param no_check_tokens: Don't look for known tokens inside ascii files.\n"
            ":param no_check_troff: Don't look for troff sequences inside ascii files.\n"
        )
    },
	{NULL}  /* Sentinel */
};

static PyTypeObject
MagicType = {
	PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "Magic",
	.tp_doc = (
	    "Open libmagic database and create a Magic instance\n\n"
        ":param debug: Print debugging messages to stderr.\n"
        ":param symlink: If the file queried is a symlink, follow it.\n"
        ":param compress: If the file is compressed, unpack it and look at the contents.\n"
        ":param devices: If the file is a block or character special \n"
        "                device, then open the device and try to look in its contents.\n"
        ":param mime_type: Return a MIME type string, instead of a textual description.\n"
        ":param mime_encoding: Return a MIME encoding, instead of a textual description.\n"
        ":param all: Return all matches, not just the first.\n"
        ":param check: Check the magic database for consistency and print warnings to stderr.\n"
        ":param preserve_atime: On systems that support utime or utimes, attempt to \n"
        "                       preserve the access time of files analyzed.\n"
        ":param raw: Don't translate unprintable characters to a \\ooo octal representation.\n"
        ":param error: Treat operating system errors while trying to open files and \n"
        "              follow symlinks as real errors, instead of printing them \n"
        "              in the magic buffer.\n"
        ":param no_check_apptype: Check for EMX application type (only on EMX).\n"
        ":param no_check_ascii: Check for various types of ascii files.\n"
        ":param no_check_compress: Don't look for, or inside compressed files.\n"
        ":param no_check_elf: Don't print elf details.\n"
        ":param no_check_fortran: Don't look for fortran sequences inside ascii files.\n"
        ":param no_check_soft: Don't consult magic files.\n"
        ":param no_check_tar: Don't examine tar files.\n"
        ":param no_check_tokens: Don't look for known tokens inside ascii files.\n"
        ":param no_check_troff: Don't look for troff sequences inside ascii files.\n"
    ),
	.tp_basicsize = sizeof(Magic),
	.tp_itemsize = 0,
	.tp_flags = Py_TPFLAGS_DEFAULT,
	.tp_new = Magic_new,
	.tp_init = (initproc) Magic_init,
	.tp_dealloc = (destructor) Magic_dealloc,
	.tp_members = Magic_members,
	.tp_methods = Magic_methods,
	.tp_repr = (reprfunc) Magic_repr
};


static PyModuleDef _magic_module = {
	PyModuleDef_HEAD_INIT,
	.m_name = "_magic",
	.m_doc = "Python libmagic c bindings.",
	.m_size = -1,
};


PyMODINIT_FUNC PyInit__magic(void) {
	PyObject *m;

	m = PyModule_Create(&_magic_module);

	if (m == NULL) return NULL;

    if (PyType_Ready(&MagicType) < 0) return NULL;
    Py_INCREF(&MagicType);
    if (PyModule_AddObject(m, "Magic", (PyObject *) &MagicType) < 0) {
        Py_XDECREF(&MagicType);
        Py_XDECREF(m);
        return NULL;
    }

	return m;
}
