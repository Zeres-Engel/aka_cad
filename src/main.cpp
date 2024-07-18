#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <libnest2d/libnest2d.hpp>

#include "../tools/printer_parts.hpp"
#include "../tools/svgtools.hpp"

namespace py = pybind11;

using Point = libnest2d::Point;
using Box = libnest2d::Box;
using Item = libnest2d::Item;
using PackGroup = libnest2d::PackGroup;
using SVGWriter = libnest2d::svg::SVGWriter<libnest2d::PolygonImpl>;

PYBIND11_MODULE(aka_cad, m)
{
    m.doc() = "2D irregular bin packaging and nesting for python";

    py::class_<Point>(m, "Point", "2D Point")
        .def(py::init<int, int>(),  py::arg("x"), py::arg("y"))
        //.def_property_readonly("x", &Point::X)
        .def_property_readonly("x", [](const Point &p) { return p.X; })
        .def_property_readonly("y", [](const Point &p) { return p.Y; })
        .def("__repr__",
             [](const Point &p) {
                 std::string r("Point(");
                 r += boost::lexical_cast<std::string>(p.X);
                 r += ", ";
                 r += boost::lexical_cast<std::string>(p.Y);
                 r += ")";
                 return r;
             }
        )
        .def("__eq__", [](const Point &p, const Point &q) { return p == q; });

    // see lib/libnest2d/include/libnest2d/geometry_traits.hpp
    py::class_<Box>(m, "Box")
        .def(py::init([](int width, int height) {
            // Giữ lại cách tạo đối tượng Box với trung tâm là trung điểm của hộp
            return std::unique_ptr<Box>(new Box(width, height, {width / 2, height / 2}));
        }), py::arg("width"), py::arg("height"))
        .def("width", [](const Box& box) {
            // Chuyển đổi width sang string sử dụng boost::lexical_cast
            return boost::lexical_cast<std::string>(box.width());
        }, "Returns the width of the box as a string")
        .def("height", [](const Box& box) {
            // Chuyển đổi height sang string sử dụng boost::lexical_cast
            return boost::lexical_cast<std::string>(box.height());
        }, "Returns the height of the box as a string")
        .def("area", [](const Box& box) {
            // Chuyển đổi area sang string sử dụng boost::lexical_cast
            return boost::lexical_cast<std::string>(box.area());
        }, "Returns the area of the box as a string");


    // Item is a shape defined by points
    // see lib/libnest2d/include/libnest2d/nester.hpp
    py::class_<Item>(m, "Item", "An item to be placed on a bin.")
        .def(py::init<std::vector<Point>>())
        .def("__repr__",
             [](const Item &i) {
                 std::string r("Item(area: ");
                 r += boost::lexical_cast<std::string>(i.area());
                 r += ", bin_id: ";
                 r += boost::lexical_cast<std::string>(i.binId());
                 r += ", vertices: ";
                 r += boost::lexical_cast<std::string>(i.vertexCount());
                 r += ")";
                 return r;
             }
        )

        .def_property_readonly("area", 
            [](const Item &i) { return boost::lexical_cast<std::string>(i.area()); }, 
            "Returns the area of the item as a string.")
        .def_property_readonly("bin_id", 
            [](const Item &i) { return boost::lexical_cast<std::string>(i.binId()); }, 
            "Returns the bin ID of the item as a string.")
        .def_property_readonly("vertex_count", 
            [](const Item &i) { return boost::lexical_cast<std::string>(i.vertexCount()); }, 
            "Returns the number of vertices of the item as a string.")
        .def_property_readonly("translation",
            [](const Item &i) {
                auto translation = i.translation();
                return std::make_pair(libnest2d::getX(translation), libnest2d::getY(translation));
            },
            "Returns the translation vector as a tuple (x, y).")
        .def_property_readonly("rotation",
            [](const Item &i) {
                return static_cast<double>(i.rotation());  // Giả sử Radians có thể chuyển đổi sang double
            },
            "Returns the rotation angle in radians.")


        .def("transformed_vertices",
             [](const Item &item) {
                 std::vector<std::pair<int, int>> vertices;
                 const auto &shape = item.transformedShape();

                 namespace sl = libnest2d::shapelike;
                 for (auto it = sl::cbegin(shape); it != sl::cend(shape); ++it) {
                     vertices.emplace_back(libnest2d::getX(*it), libnest2d::getY(*it));
                 }
                 return vertices;
             },
             "Returns a list of tuples representing the coordinates of all vertices after transformation."
        )
        .def("item_id",
            [](const Item &item) {
                std::string item_id;
                const auto &shape = item.rawShape();

                namespace sl = libnest2d::shapelike;
                for (auto it = sl::cbegin(shape); it != sl::cend(shape); ++it) {
                    item_id += "(" + std::to_string(libnest2d::getX(*it)) + "," + std::to_string(libnest2d::getY(*it)) + ")";
                }
                return item_id;
            },
            "Returns a string representing the coordinates of all raw vertices to use as an item ID."
        )
        .def("raw_vertices",
             [](const Item &item) {
                 std::vector<std::pair<int, int>> vertices;
                 const auto &shape = item.rawShape();

                 namespace sl = libnest2d::shapelike;
                 for (auto it = sl::cbegin(shape); it != sl::cend(shape); ++it) {
                     vertices.emplace_back(libnest2d::getX(*it), libnest2d::getY(*it));
                 }
                 return vertices;
             },
             "Returns a list of tuples representing the coordinates of all raw vertices."
        );

    m.def("nest", [](std::vector<Item>& input, std::vector<Box>& boxes) {
        std::vector<Item> output;
        for (size_t i = 0; i < boxes.size(); i++) {
            nest(input, boxes[i]); // Giả sử nest này làm việc với binId của mỗi Item
            std::vector<Item> remainingItems;

            for (Item& itm : input) {
                if (itm.binId() == 0) {
                    itm.binId(i);
                    output.emplace_back(itm);
                } else {
                    remainingItems.emplace_back(itm);
                }
            }

            input = std::move(remainingItems);
        }

        for (Item& itm : input) {
            itm.binId(-1);
            output.emplace_back(itm);
        }

        // Helper function to generate item_id
        auto generateItemId = [](const Item& item) {
            std::string item_id;
            const auto& shape = item.rawShape();
            for (auto it = libnest2d::shapelike::cbegin(shape); it != libnest2d::shapelike::cend(shape); ++it) {
                item_id += "(" + std::to_string(libnest2d::getX(*it)) + "," + std::to_string(libnest2d::getY(*it)) + ")";
            }
            return item_id;
        };

        // Sort output based on item_id
        std::sort(output.begin(), output.end(), [&generateItemId](const Item& a, const Item& b) {
            return generateItemId(a) < generateItemId(b);
        });

        return output;
    },
    py::return_value_policy::reference_internal,
    py::arg("input"), 
    py::arg("boxes"),
    "Nest and pack the input items into the provided list of box bins, and sort them by item_id."
    );
}