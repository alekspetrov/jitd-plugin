/**
 * User Routes - GET endpoint example
 *
 * @route GET /api/users/:id
 * @access Private
 */

import { Router, Request, Response, NextFunction } from 'express';
import { authMiddleware } from '../middleware/auth';

const router = Router();

/**
 * GET /api/users/:id
 * @description Get user by ID
 * @access Private
 */
router.get(
  '/api/users/:id',
  authMiddleware,
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const { id } = req.params;

      // TODO: Fetch user from database
      const user = await getUserById(id);

      if (!user) {
        return res.status(404).json({
          success: false,
          error: 'User not found',
        });
      }

      res.status(200).json({
        success: true,
        data: user,
      });
    } catch (error) {
      next(error);
    }
  }
);

export default router;

// Mock function (replace with actual database query)
async function getUserById(id: string) {
  return {
    id,
    name: 'John Doe',
    email: 'john@example.com',
  };
}
