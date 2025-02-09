import React, { useState, useEffect } from "react";
import axios from "axios";
import "./StudentTable.css";

const StudentTable = () => {
    const [students, setStudents] = useState([]);
    const [page, setPage] = useState(1);
    const [size, setSize] = useState(10);
    const [total, setTotal] = useState(0);
    const [newStudent, setNewStudent] = useState({
        first_name: "",
        last_name: "",
        patronymic: "",
        group: "",
        grade: 1,
        faculty: "",
    });

    useEffect(() => {
        axios
            .get(`http://0.0.0.0:8000/students?page=${page}&size=${size}`)
            .then((response) => {
                setStudents(response.data.data);
                setTotal(response.data.total);
            });
    }, [page, size]);

    const totalPages = Math.ceil(total / size);

    const renderPageNumbers = () => {
        const pageNumbers = [];
        const maxVisiblePages = 5;

        // Определяем, какие страницы показывать
        let startPage = Math.max(page - Math.floor(maxVisiblePages / 2), 1);
        let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

        if (endPage - startPage < maxVisiblePages - 1) {
            startPage = Math.max(endPage - maxVisiblePages + 1, 1);
        }

        for (let i = startPage; i <= endPage; i++) {
            pageNumbers.push(
                <button
                    key={i}
                    className={`page-number ${i === page ? "active" : ""}`}
                    onClick={() => setPage(i)}
                >
                    {i}
                </button>
            );
        }

        if (endPage < totalPages) {
            pageNumbers.push(
                <span key="dots" className="dots">
          ...
        </span>
            );
            pageNumbers.push(
                <button
                    key={totalPages}
                    className="page-number"
                    onClick={() => setPage(totalPages)}
                >
                    {totalPages}
                </button>
            );
        }

        return pageNumbers;
    };

    const handleAddStudent = () => {
        axios
            .post("http://0.0.0.0:8000/students/", newStudent)
            .then((response) => {
                alert(response.data.message);
                window.location.reload();
            })
            .catch((error) => console.error(error));
    };

    const handleDeleteStudent = (id) => {
        axios
            .delete(`http://0.0.0.0:8000/students/${id}`)
            .then((response) => {
                alert(response.data.message);
                window.location.reload();
            })
            .catch((error) => console.error(error));
    };

    return (
        <div className="student-table-container">
            <h1>Список студентов</h1>
            <table className="student-table">
                <thead>
                <tr>
                    <th>Имя</th>
                    <th>Фамилия</th>
                    <th>Отчество</th>
                    <th>Группа</th>
                    <th>Курс</th>
                    <th>Факультет</th>
                    <th>Отчислить?</th>
                </tr>
                </thead>
                <tbody>
                {students.map((student) => (
                    <tr key={student.id}>
                        <td>{student.first_name}</td>
                        <td>{student.last_name}</td>
                        <td>{student.patronymic}</td>
                        <td>{student.group}</td>
                        <td>{student.grade}</td>
                        <td>{student.faculty}</td>
                        <td>
                            <button onClick={() => handleDeleteStudent(student.id)}>Отчислить</button>
                        </td>
                    </tr>
                ))}
                </tbody>
            </table>
            <div className="pagination-container">
                <button
                    className="page-button"
                    disabled={page === 1}
                    onClick={() => setPage(page - 1)}
                >
                    &laquo;
                </button>
                {renderPageNumbers()}
                <button
                    className="page-button"
                    disabled={page === totalPages}
                    onClick={() => setPage(page + 1)}
                >
                    &raquo;
                </button>
                <select
                    className="page-size-selector"
                    value={size}
                    onChange={(e) => setSize(Number(e.target.value))}
                >
                    <option value={5}>5 / стр.</option>
                    <option value={10}>10 / стр.</option>
                    <option value={20}>20 / стр.</option>
                </select>
            </div>
            <h2>Добавить студента</h2>
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleAddStudent();
                }}
            >
                <input
                    type="text"
                    placeholder="Имя"
                    value={newStudent.first_name}
                    onChange={(e) =>
                        setNewStudent({...newStudent, first_name: e.target.value})
                    }
                />
                <input
                    type="text"
                    placeholder="Фамилия"
                    value={newStudent.last_name}
                    onChange={(e) =>
                        setNewStudent({...newStudent, last_name: e.target.value})
                    }
                />
                <input
                    type="text"
                    placeholder="Отчество"
                    value={newStudent.patronymic}
                    onChange={(e) =>
                        setNewStudent({...newStudent, patronymic: e.target.value})
                    }
                />
                <input
                    type="text"
                    placeholder="Группа"
                    value={newStudent.group}
                    onChange={(e) =>
                        setNewStudent({...newStudent, group: e.target.value})
                    }
                />
                <input
                    type="number"
                    placeholder="Курс"
                    value={newStudent.grade}
                    onChange={(e) => {
                        const value = parseInt(e.target.value);
                        if (value >= 1 && value <= 5) {
                            setNewStudent({...newStudent, grade: value});
                        }
                    }}
                    min="1"
                    max="5"
                />
                <input
                    type="text"
                    placeholder="Факультет"
                    value={newStudent.faculty}
                    onChange={(e) =>
                        setNewStudent({...newStudent, faculty: e.target.value})
                    }
                />
                <button type="submit">Добавить</button>
            </form>
        </div>
    );
};

export default StudentTable;
