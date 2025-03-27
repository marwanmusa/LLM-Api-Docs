export const apiDocs = [
  {
    id: 'example',
    name: 'Example API',
    baseUrl: 'https://api.example.com/v1',
    description: 'This is an example API for demonstration purposes.',
    endpoints: [
      {
        method: 'GET',
        path: '/items',
        description: 'Retrieve a list of items.',
        parameters: [],
        exampleResponse: [
          { id: 1, name: "Item One" },
          { id: 2, name: "Item Two" }
        ]
      },
      {
        method: 'POST',
        path: '/items',
        description: 'Create a new item.',
        parameters: [
          { name: 'name', type: 'string', description: 'Name of the item to create.' }
        ],
        exampleResponse: { id: 3, name: "New Item" }
      }
    ]
  },
  {
    id: 'other',
    name: 'Other API',
    baseUrl: 'https://api.other.com/v2',
    description: 'This API is another example with different endpoints.',
    endpoints: [
      {
        method: 'GET',
        path: '/widgets',
        description: 'List all widgets.',
        parameters: [],
        exampleResponse: [
          { id: 'a1', name: "Widget A" },
          { id: 'b2', name: "Widget B" }
        ]
      }
    ]
  }
]; 