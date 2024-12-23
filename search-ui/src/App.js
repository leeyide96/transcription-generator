import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildFacetConfigFromConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields
} from "./config/config-helper";

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "cv-transcriptions"
});
const config = {
  searchQuery: {
    search_fields: {
      generated_text: {
        weight: 3
      }
    },
    result_fields: {
      filename: {
        snippet: {}
      },
      generated_text: {
        snippet: {}
      },
      duration: {
        snippet: {}
      },
      age: {
        snippet: {}
      },
      gender: {
        snippet: {}
      },
      accent: {
        snippet: {}
      }
    },
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox/>}
                  sideContent={
                  <div>
                    {wasSearched && <Sorting label={"Sort by"} sortOptions={[{name: "filename", value: [{field: "filename.keyword", direction: "asc"}]},
                                                                            {name: "generated_text", value: [{field: "generated_text.keyword", direction: "asc"}]}]} />}
                  </div>}
                  bodyContent={
                    <Results
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
