/**
 * ${COMPONENT_NAME} - ${DESCRIPTION}
 */

import React from 'react';
${STYLE_IMPORT}

${PROPS_INTERFACE}

export const ${COMPONENT_NAME}: React.FC<${PROPS_INTERFACE}> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div className={`${styles.container} ${className || ''}`}>
      {children}
    </div>
  );
};
