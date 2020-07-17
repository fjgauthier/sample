"""
Code sample
"""
import sqlite3

import numpy


class Select:
    shapes_sql = """
        SELECT s.shape_id, s.shape_name, p.x, p.y, p.z
        FROM [shapes] s
        JOIN [shapesPointsAssoc] spa on s.shape_id = spa.shape_id
        JOIN [points] p on spa.point_id = p.point_id
        ORDER BY s.shape_id, spa.ordinal
    """

    create_database_sql = [
        """
        CREATE TABLE [points](
            [point_id] INTEGER IDENTITY (1, 1) NOT NULL PRIMARY KEY,
            [x] FLOAT,
            [y] FLOAT,
            [z] FLOAT
        )
        """,
        """
        CREATE TABLE [shapesPointsAssoc](
            [shape_point_assoc_id] INTEGER IDENTITY (1, 1) NOT NULL PRIMARY KEY,
            [shape_id] INTEGER NOT NULL,
            [point_id] INTEGER NOT NULL,
            [ordinal] INTEGER NOT NULL,
            CONSTRAINT FK_shapesPointsAssoc_points
                FOREIGN KEY ([point_id])
                REFERENCES [points] ([point_id])
        )
        """,
        """
        CREATE TABLE [shapes](
            [shape_id] INTEGER IDENTITY (1, 1) NOT NULL PRIMARY KEY,
            [shape_name] NVARCHAR(128),
            CONSTRAINT FK_shapes_shapesPointsAssoc
                FOREIGN KEY ([shape_id])
                REFERENCES [shapesPointsAssoc] ([shape_id])
        )
        """,
    ]


def dict_factory(cursor, row):
    d = {}
    for index, col in enumerate(cursor.description):
        d[col[0]] = row[index]
    return d


class SampleError(Exception):
    pass


class Shape:
    def __init__(self, shape_id, shape_name):
        self.shape_id = shape_id
        self.shape_name = shape_name
        self.points = []

    def add_point(self, x, y, z):
        self.points.append([x, y, z])

    def centroid(self):
        if not len(self.points):
            raise ZeroDivisionError("Unable to compute with 0 data")

        array = numpy.array(self.points)
        computed_centroid = numpy.sum(array, axis=0) / len(self.points)
        return computed_centroid


class Sample:
    def __init__(self, database_file):
        self.connection = None
        self.database_file = database_file
        self.shapes = {}  # shape id: shape

        self.connect()

    def __iter__(self):
        return self.shapes.values()

    def __len__(self):
        return len(self.shapes)

    def connect(self):
        self.connection = sqlite3.connect(self.database_file)
        self.connection.execute("PRAGMA foreign_keys = 1")

    def create_empty_database(self):
        for table_create_statement in Select.create_database_sql:
            try:
                self.connection.execute(table_create_statement)
            except sqlite3.Error:
                print(f"error with statement {table_create_statement}")
                raise
        self.connection.commit()

    def load_database(self):
        self.connection.row_factory = dict_factory
        cursor = self.connection.cursor()
        cursor.execute(Select.shapes_sql)

        # At this point empty shapes
        self.shapes.clear()
        for shape_point in cursor:
            self.shapes.setdefault(shape_point['shape_id'], Shape(shape_point['shape_id'], shape_point['shape_name']))\
                .add_point(shape_point['x'], shape_point['y'], shape_point['z'])

    def add_shape(self, shape):
        if not isinstance(shape, Shape):
            raise SampleError("Sample can only use Shapes")
        self.shapes[shape.shape_id] = shape
