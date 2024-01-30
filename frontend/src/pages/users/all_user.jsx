import React, { Fragment, useCallback, useState } from "react";
import { Breadcrumbs, Btn, H4 } from "../../AbstractElements";
import { Card, CardBody, Container } from "reactstrap";
import DataTable from "react-data-table-component";
import { dummytabledata, tableColumns } from "../../Data/Table/Defaultdata";

const GetUsers = () => {
  const [selectedRows, setSelectedRows] = useState([]);
  const [toggleDelet, setToggleDelet] = useState(false);
  const [data, setData] = useState(dummytabledata);

  const handleRowSelected = useCallback((state) => {
    setSelectedRows(state.selectedRows);
  }, []);

  const handleDelete = () => {
    if (
      window.confirm(
        `Are you sure you want to delete:\r ${selectedRows.map(
          (r) => r.title
        )}?`
      )
    ) {
      setToggleDelet(!toggleDelet);

      setData(
        data.filter((item) =>
          selectedRows.filter((elem) => elem.id === item.id).length > 0
            ? false
            : true
        )
      );
      setSelectedRows("");
    }
  };
  return (
    <Fragment>
      <Breadcrumbs
        parent="Users"
        title="All Users"
        subParent="Profile"
        mainTitle="All Users"
      />
      <Container fluid={true}>
        <Card>
          <CardBody>
            {selectedRows.length !== 0 && (
              <div
                className={`d-flex align-items-center justify-content-between bg-light-info p-2`}
              >
                <H4 attrH4={{ className: "text-muted m-0" }}>
                  Delet Selected Data..!
                </H4>
                <Btn
                  attrBtn={{ color: "danger", onClick: () => handleDelete() }}
                >
                  Delete
                </Btn>
              </div>
            )}
            <DataTable
              data={data}
              columns={tableColumns}
              striped={true}
              center={true}
              pagination
              selectableRows
              onSelectedRowsChange={handleRowSelected}
              clearSelectedRows={toggleDelet}
            />
          </CardBody>
        </Card>
      </Container>
    </Fragment>
  );
};
export default GetUsers;
